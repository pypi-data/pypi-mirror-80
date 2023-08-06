#  Copyright 2020 Regents of the University of Minnesota.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import os
import sys
import urllib.request
from argparse import ArgumentParser
from pathlib import Path
from shutil import rmtree
from subprocess import Popen, STDOUT, PIPE
from tempfile import NamedTemporaryFile
from threading import Thread
from time import sleep
from zipfile import ZipFile

import grpc
from tqdm import tqdm

from biomedicus.config import load_config


def _listen(process: Popen) -> int:
    for line in process.stdout:
        print(line.decode(), end='', flush=True)
    return process.wait()


def check_data(download=False):
    try:
        data = Path(os.environ['BIOMEDICUS_DATA'])
    except KeyError:
        data = Path.home() / '.biomedicus' / 'data'
        os.environ['BIOMEDICUS_DATA'] = str(data)

    config = load_config()
    download_url = config['data.data_url']
    data_version = config['data.version']
    version_file = data / 'VERSION.txt'
    if not data.exists():
        print('No existing data folder.')
    elif not version_file.exists():
        print('No existing version file.')
    else:
        existing_version = version_file.read_text().strip()
        if existing_version != data_version:
            print('Data folder ({}) is not most recent version ({})'.format(existing_version,
                                                                            data_version))
        else:
            print('Data folder is up to date version {}'.format(data_version))
            return
    if not download:
        print(
            'It looks like you do not have the set of models distributed for BioMedICUS.\n'
            'The models are available from our website (https://nlpie.umn.edu/downloads)\n'
            'and can be installed by specifying the environment variable BIOMEDICUS_DATA\n'
            'or by placing the extracted models in ~/.biomedicus/data'
        )
        prompt = 'Would you like to download the model files to {} (Y/N)? '.format(str(data))
        download = input(prompt) in ['Y', 'y', 'Yes', 'yes']
    if download:
        download_data_to(download_url, data)
    else:
        exit()


def download_data_to(download_url, data):
    def report(_, read, total):
        if report.bar is None:
            report.bar = tqdm(total=total, unit='b', unit_scale=True, unit_divisor=10 ** 6)
        report.bar.update(read)

    report.bar = None
    try:
        with NamedTemporaryFile() as temporary_file:
            print('Starting download: ', download_url)
            urllib.request.urlretrieve(download_url, filename=temporary_file.name,
                                       reporthook=report)
            if data.exists():
                rmtree(str(data))
            data.mkdir(parents=True, exist_ok=False)
            with ZipFile(temporary_file) as zf:
                print('Extracting...')
                zf.extractall(path=str(data))
    finally:
        if report.bar is not None:
            report.bar.close()


def deploy(conf):
    try:
        check_data(conf.download_data)
    except ValueError:
        return
    jar_path = str(Path(__file__).parent.parent / 'biomedicus-all.jar')
    python_exe = sys.executable
    calls = [
        ([python_exe, '-m', 'biomedicus.sentences.bi_lstm', 'processor'],
         conf.sentences_port),

        (['java', '-Xms128m', '-Xmx8g', '-cp', jar_path,
          'edu.umn.biomedicus.tagging.tnt.TntPosTaggerProcessor'], conf.tagger_port),
    ]
    host = conf.host
    if host is None:
        host = '127.0.0.1'
    if conf.events_address is None:
        calls.insert(0, ([python_exe, '-m', 'mtap', 'events'], conf.events_port))
        events_address = host + ':' + conf.events_port
    else:
        events_address = conf.events_address

    for i, (call, port) in enumerate(calls):
        call.extend(['-p', port])
        call.extend(['--workers', str(conf.workers)])
        if conf.events_address is not None or i > 0:
            call.extend(['--events', events_address])
        if conf.discovery:
            call.append('--register')
        if conf.host:
            call.extend(['--host', conf.host])
    process_listeners = []
    processes = []
    for call, port in calls:
        p = Popen(call, stdout=PIPE, stderr=STDOUT)
        listener = Thread(target=_listen, args=(p,))
        listener.start()
        process_listeners.append(listener)
        processes.append(p)
        with grpc.insecure_channel(host + ':' + port) as channel:
            future = grpc.channel_ready_future(channel)
            try:
                future.result(timeout=60)
            except grpc.FutureTimeoutError:
                print('Failed to launch: {}'.format(call))
                exit()

    print('Done starting all processors', flush=True)
    try:
        while True:
            sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        print("Shutting down all processors")
        for listener in process_listeners:
            listener.join(timeout=1)

    print("Done shutting down all processors")


def main(args=None):
    parser = ArgumentParser()
    parser.add_argument('--config-file')
    parser.add_argument('--host', default=None,
                        help='A host address to bind all of the services to.')
    parser.add_argument('--discovery', action='store_true',
                        help='Register the services with consul.')
    parser.add_argument('--events-address', default=None,
                        help="An existing events service to use instead of launching one.")
    parser.add_argument('--events-port', default='10100',
                        help="The port to launch the events service on")
    parser.add_argument('--sentences-port', default='10102',
                        help="The port to launch the sentences processor on.")
    parser.add_argument('--tagger-port', default='10103',
                        help="The port to launch the tnt pos tagger on.")
    parser.add_argument('--workers', default=4, type=int,
                        help="Number of worker threads for processors and events service.")
    parser.add_argument('--download-data', action='store_true',
                        help="If this flag is specified, automatically download the biomedicus "
                             "data if it is missing.")

    conf = parser.parse_args(args)
    deploy(conf)


if __name__ == '__main__':
    main()

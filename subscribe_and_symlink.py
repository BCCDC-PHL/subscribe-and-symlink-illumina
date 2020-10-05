#!/usr/bin/env python

import argparse
import json
import re
import os
import sys

import zmq
import zmq.auth


def create_symlinks(source_directory, destination_directory):
    created_symlinks = []
    for fastq_file in os.listdir(source_directory):
        source_fastq_path = os.path.join(source_directory, fastq_file)
        destination_fastq_path = os.path.join(destination_directory, fastq_file)
        os.symlink(source_fastq_path, destination_fastq_path)
        created_symlinks.append(destination_fastq_path)

    return created_symlinks


def main(args):

    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    client_secret_file = args.private_key
    client_public, client_secret = zmq.auth.load_certificate(client_secret_file)
    socket.curve_secretkey = client_secret
    socket.curve_publickey = client_public
    server_public_file = args.public_key
    server_public, _ = zmq.auth.load_certificate(server_public_file)
    socket.curve_serverkey = server_public
    print("Collecting updates from server...")
    socket.connect("tcp://127.0.0.1:%s" % args.port)

    socket.subscribe(args.topic)

    while True:
        topic, message = socket.recv_string().split(' ', 1)
        if topic == 'illumina_runs':
            try:
                message = json.loads(message)
            except Exception as e:
                print('Error parsing message: ' + e)

            if message['event'] == 'run_directory_created':
                experiment_name_matched = re.match(args.experiment_name_regex, message['experiment_name'])
                if experiment_name_matched:
                    run_directory = message['path'].split('/')[-1]
                    original_run_directory_path = os.path.normpath(message['path'])
                    original_run_directory_fastq_path = os.path.join(original_run_directory_path, 'Data', 'Intensities', 'BaseCalls')
                    symlink_run_directory_path = os.path.join(args.symlink_directory, run_directory)
                    os.makedirs(symlink_run_directory_path, exist_ok=True)
                    create_symlinks(original_run_directory_fastq_path, symlink_run_directory_path)
            else:
                pass
                # print(json.dumps(message))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=5556)
    parser.add_argument('--topic', default="illumina_runs")
    parser.add_argument('--experiment_name_regex', default=".+")
    parser.add_argument('--symlink_directory', default=".")
    parser.add_argument('--public_key', required=True)
    parser.add_argument('--private_key', required=True)
    args = parser.parse_args()
    main(args)

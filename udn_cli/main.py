import argparse
from datetime import datetime
from .config import SingleUploadConfig, MultiUploadConfig
from .commands import UploadSingle, UploadMultiple
import logging


def setup_log_file(command_name):
    now = datetime.now().strftime('%Y%m%d-%s')
    log_file_name = '{command}-{time}.log'.format(
        command=command_name,
        time=now)
    logging.basicConfig(filename=log_file_name, level=logging.INFO)


def handle_multi_upload(args):
    setup_log_file('multi-upload')
    config = MultiUploadConfig(args)
    uploader = UploadMultiple(config)
    uploader.upload()


def handle_single_upload(args):
    setup_log_file('upload')
    config = SingleUploadConfig(args)
    uploader = UploadSingle(config)
    uploader.upload()


def main():
    # setup command line args
    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers()

    # setup 'upload' command
    single_upload_parser = sub_parsers.add_parser('upload')
    single_upload_parser.add_argument('file_path')
    single_upload_parser.add_argument('seq_request_id')
    single_upload_parser.add_argument('patient_uuid')
    single_upload_parser.add_argument('--metadata')
    single_upload_parser.add_argument('--test', action="store_true")
    single_upload_parser.add_argument('--force', action="store_true")
    single_upload_parser.set_defaults(handler=handle_single_upload)

    # setup 'upload-dir' command
    multi_upload_parser = sub_parsers.add_parser('multi-upload')
    multi_upload_parser.add_argument('directory')
    multi_upload_parser.add_argument('--test', action="store_true")
    multi_upload_parser.add_argument('--force', action="store_true")
    multi_upload_parser.set_defaults(handler=handle_multi_upload)

    # build config and run
    args = parser.parse_args()
    args.handler(args)

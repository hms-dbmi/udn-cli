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
    parser = argparse.ArgumentParser(description='CLI tool for UDN sequencing file uploads')
    sub_parsers = parser.add_subparsers()

    # setup 'upload' command
    single_upload_parser = sub_parsers.add_parser('upload', help='upload help')
    single_upload_parser.add_argument('file_path', help='Local path to file')
    single_upload_parser.add_argument('seq_request_id', help='Sequence Request ID for file association')
    single_upload_parser.add_argument('patient_uuid', help='Patient UUID for file association')
    single_upload_parser.add_argument('--bucket', help='S3 bucket for data storage')
    single_upload_parser.add_argument('--metadata',
                                      help='Any extra metadata to store with the file; Needs to be JSON format')
    single_upload_parser.add_argument('--test', action="store_true", help='Use development server')
    single_upload_parser.add_argument('--force', action="store_true",
                                      help='Force upload and overwrite existing file with same filename')
    single_upload_parser.set_defaults(handler=handle_single_upload)

    # setup 'upload-dir' command
    multi_upload_parser = sub_parsers.add_parser('multi-upload', help='multi-upload help')
    multi_upload_parser.add_argument('directory', help='Local directory of files to upload')
    multi_upload_parser.add_argument('--test', action="store_true", help='Use development server')
    multi_upload_parser.add_argument('--force', action="store_true",
                                     help='Force upload and overwrite existing files with same filenames')
    multi_upload_parser.set_defaults(handler=handle_multi_upload)

    # build config and run
    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()

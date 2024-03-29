import os
import time
import json
import hashlib
import requests
from urllib.parse import urljoin
import boto3


class UploadManager:
    def __init__(self, config):
        self._config = config
        self._permissions = config.permissions

    def upload(self):
        try:
            start_time = time.time()
            (secret_key, access_key, session_token, folder_name,
             location_id, fs_uuid) = self._configure_upload()

            self._run_multipart_upload(
                secret_key, access_key, session_token, folder_name)

            self._mark_upload_as_complete(location_id, fs_uuid)

            end_time = time.time()
            upload_time = round(end_time - start_time, 2)

            success_msg = (
                'SUCCESS: {file_name} uploaded to {bucket}/{folder_name}, '
                'time: {upload_time} seconds')

            message = success_msg.format(
                file_name=self._file_name,
                bucket=self._config.bucket,
                folder_name=folder_name,
                upload_time=upload_time)

            print(message)
            return message

        except Exception as e:
            exception_message = 'FAILED: {file_name}, reason: {reason}'.format(
                file_name=self._file_name,
                reason=e)
            print(exception_message)
            return exception_message

    def __call__(self):
        return self.upload()

    def _configure_upload(self):
        # manage file records on the UDN side but this API endpoint
        # calls FileService to create the storage location in the cloud
        udn_api_url = urljoin(self._config.host, 'api/sequence/file/')
        header = self._get_udn_api_header()
        data = self._build_data_payload()

        response = requests.post(
            udn_api_url,
            headers=header,
            data=json.dumps(data))

        secret_key = response.json().get('secret_key')
        access_key = response.json().get('access_key')
        session_token = response.json().get('session_token')
        folder_name = response.json().get('folder_name')
        location_id = response.json().get('location_id')
        fs_uuid = response.json().get('fs_uuid')
        error = response.json().get('error')

        # The file already exists.
        if response.status_code == 202:
            # Raise the 'exists' error only if the user didn't set --force.
            if not self._config.force:
                raise Exception(error)

        # Something went wrong registering the file with FS or the gateway.
        if response.status_code == 500:
            raise Exception(error)

        if response.status_code > 299:
            print('Warning: {error}'.format(error=response.json()['error']))

        return (secret_key, access_key, session_token,
                folder_name, location_id, fs_uuid)

    def _get_udn_api_header(self):
        udn_auth = 'Token ' + self._config.udn_token
        fs_auth = 'FSToken ' + self._config.fileservice_token

        return {
            'Authorization': udn_auth,
            'FSAuthorization': fs_auth,
            'Content-Type': 'application/json'
        }

    def _build_data_payload(self):
        return {
            'filename': self._file_name,
            'patient_uuid': self._patient_uuid,
            'sequence_id': self._seq_request_id,
            'site': self._site,
            'bucket': self._config.bucket,
            'metadata': self._metadata,
            'permissions': self._permissions
        }

    def _run_multipart_upload(
            self, secret_key, access_key, session_token, folder_name):
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                aws_session_token=session_token)

            KB = 1024
            MB = KB * KB
            transfer_config = boto3.s3.transfer.TransferConfig(
                multipart_threshold=25 * MB,
                max_concurrency=10,
                multipart_chunksize=25 * MB,
                use_threads=True)
            transfer_handle = boto3.s3.transfer.S3Transfer(
                client=s3_client,
                config=transfer_config)

            location_key = '{folder_name}/{file_name}'.format(
                folder_name=folder_name,
                file_name=self._file_name)

            transfer_handle.upload_file(
                self._file_path, self._config.bucket, location_key)
        except Exception as exc:
            err_msg = 'Failed to upload file to S3 with error: {exc}. Please try again.'.format(
                exc=exc)
            raise Exception(err_msg)

    def _mark_upload_as_complete(self, location_id, fs_uuid):
        udn_api_url = urljoin(
            self._config.host, 'api/sequence/file/mark_uploaded/')
        header = self._get_udn_api_header()
        data = {'fs_uuid': fs_uuid,
                'location_id': location_id}

        response = requests.post(
            udn_api_url, headers=header, data=json.dumps(data))

        if response.status_code != 200:
            raise Exception(
                'Failed to mark the file has having been uploaded.')

    def _validate_metadata(self, json_data):
        if 'metadata' not in json_data:
            exception_message = 'FAILED: {file_name}, reason: Provided JSON is missing metadata'.format(
                file_name=self._file_name)
            raise Exception(exception_message)

        if 'assembly' not in json_data['metadata'] or not json_data['metadata']['assembly']:
            exception_message = 'FAILED: {file_name}, reason: Provided JSON metadata must include the assembly field'.format(
                file_name=self._file_name)
            raise Exception(exception_message)

        if 'coverage' not in json_data['metadata'] or not json_data['metadata']['coverage']:
            exception_message = 'FAILED: {file_name}, reason: Provided JSON metadata must include the coverage field'.format(
                file_name=self._file_name)
            raise Exception(exception_message)

    def _get_file_md5_hash(self, file_name, directory=None):
        hash_md5 = hashlib.md5()

        if directory:
            path = os.path.json(directory, file_name)
        else:
            path = file_name

        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)

        return hash_md5.hexdigest()


class SingleUploadManager(UploadManager):
    def __init__(self, config):
        super().__init__(config)

        self._file_name = config.file_name

        json_file_name = '{filename}.json'.format(filename=config.file_name)
        with open(json_file_name) as json_file:
            json_data = json.load(json_file)

        self._validate_metadata(json_data)
        json_data['metadata']['md5'] = self._get_file_md5_hash(
            config.file_name)

        self._file_path = config.file_path
        self._patient_uuid = json_data['patient_uuid']
        self._seq_request_id = json_data['seq_request_id']
        self._metadata = json_data['metadata']
        self._site = json_data['site']


class MultiUploadManager(UploadManager):
    def __init__(self, config, file_name):
        super().__init__(config)

        metadata_file_name = file_name + '.json'
        metadata_file_path = os.path.join(config.directory, metadata_file_name)

        with open(metadata_file_path) as metadata_file:
            metadata = json.load(metadata_file)

        self._validate_metadata(json_data)
        json_data['metadata']['md5'] = self._get_file_md5_hash(
            file_name, config.directory)

        self._file_name = file_name
        self._file_path = os.path.join(config.directory, file_name)
        self._patient_uuid = metadata['patient_uuid']
        self._seq_request_id = str(metadata['seq_request_id'])
        self._metadata = metadata['metadata']

import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from .upload import SingleUploadManager, MultiUploadManager


class UploadSingle:
    def __init__(self, config):
        self._config = config

    def upload(self):
        upload_manager = SingleUploadManager(self._config)
        result = upload_manager.upload()
        logging.info(result)


class UploadMultiple:
    MAX_WORKERS = 2

    def __init__(self, config):
        self._config = config

    def upload(self):
        thread_pool = ThreadPoolExecutor(max_workers=self.MAX_WORKERS)

        # setup an upload task for each of the files to be uploaded
        tasks = []
        for file_name in os.listdir(self._config.directory):
            if file_name[-5:] == '.json':
                continue
            upload_manager = MultiUploadManager(self._config, file_name)
            tasks.append(thread_pool.submit(upload_manager))

        # wait for the tasks to complete
        for task in as_completed(tasks):
            result = task.result()
            logging.info(result)

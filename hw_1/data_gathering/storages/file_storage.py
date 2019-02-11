import json

from storages.storage import Storage

class FileStorage(Storage):

    def __init__(self, file_name):
        self.file_name = file_name

    def write_data(self, data_json):
        """
        :param data_array: collection of strings that
        should be written as lines
        """
        with open(self.file_name, 'w') as outfile:
            json.dump(data_json, outfile)

    def read_data(self):
        raise NotImplementedError

    def append_data(self, data):
        raise NotImplementedError

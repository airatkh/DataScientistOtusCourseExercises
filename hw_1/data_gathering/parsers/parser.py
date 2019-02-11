import pandas as pd


class Parser(object):
    def __init__(self, storage):
        self.storage = storage

    def parse(self, table_format_file):
        """
        Transform gathered data from json file to pandas DataFrame
        and save as csv

        :param table_format_file: file_name save to csv
        """
        pd_data = pd.read_json(self.storage.file_name)
        pd_data.to_csv(table_format_file)

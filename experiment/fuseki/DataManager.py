import pip._vendor.requests as requests  # A problem in VSCode
import pathlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from random import shuffle
import os
from alive_progress import alive_bar


class DataManager:
    def __init__(self, endpoint_list=None, data_dir=None, file_list=None):
        self._endpoint_list = endpoint_list
        self._data_dir = data_dir
        self._file_list = file_list
        self.__file_path_list = None
        self._endpoint_file_dict = None

        if None not in [self.data_dir, self.file_list]:
            self.__create_file_path_list()

        if None not in [self._endpoint_list, self.__file_path_list]:
            self._endpoint_file_dict = self.__create_endpoint_file_dict()

    def reset_default_graph_all(self):
        if self._endpoint_file_dict is not None:
            for endpoint, file_path in self._endpoint_file_dict.items():
                self.reset_default_graph(endpoint=endpoint, file_path=file_path)
        else:
            raise ValueError(
                f"endpoint_file_dict is None:\
                {self.endpoint_file_dict}"
            )

    def reset_default_graph(self, endpoint, file_path):
        self.drop_default_graph(endpoint=endpoint)
        self.upload_file(endpoint=endpoint, file_path=file_path)
        return True

    def upload_file(self, endpoint, file_path, format="turtle", charset="latin-1"):
        data = open(file_path).read()
        if format == "turtle":
            headers = {"Content-Type": "text/turtle"}
        elif format == "owl":
            headers = {"Content-Type": "application/rdf+xml"}

        with open(file_path, "r", encoding=charset) as file:
            data = file.read()
            r = requests.post(endpoint, data=data, headers=headers)

    def drop_default_graph(self, endpoint):
        query = "DROP DEFAULT"
        headers = {"Content-Type": "application/sparql-update"}
        r = requests.post(endpoint, data=query, headers=headers)

    def send_multiple_updates(self, endpoint_query_pair):
        results = []
        shuffle(endpoint_query_pair)
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = executor.map(self.update, endpoint_query_pair)
            for result in futures:
                results.append(result)
        return results

    # Helper methods
    def __get_path(self, file_name):
        if self._data_dir is None:
            raise ValueError(f"dir_name is None: {self._data_dir}")
        if file_name is None:
            raise ValueError(f"file_name is None: {file_name}")

        return str(pathlib.Path.home().joinpath(self._data_dir, file_name))

    def __create_file_path_list(self):
        self.__file_path_list = list(map(self.__get_path, self._file_list))

    def __create_endpoint_file_dict(self):
        return dict(zip(self._endpoint_list, self.__file_path_list))

    # def reset_default_graph_concurrent(self):
    #     results = []
    #     endpoint_list, file_list = zip(*self._endpoint_file_dict.items())
    #     with ThreadPoolExecutor(max_workers=10) as executor:
    #         futures = executor.map(self.reset_default_graph,
    #                                 endpoint_list,
    #                                 file_list)
    #         for result in futures:
    #             results.append(result)
    #     return results

    # Getters
    @property
    def endpoint_list(self):
        return self._endpoint_list

    @property
    def data_dir(self):
        return self._data_dir

    @property
    def file_list(self):
        return self._file_list

    @property
    def endpoint_file_dict(self):
        return self._endpoint_file_dict

    # Setters
    @endpoint_list.setter
    def endpoint_list(self, value):
        self._endpoint_list = value

    @data_dir.setter
    def data_dir(self, value):
        self._data_dir = value

    @file_list.setter
    def file_list(self, value):
        self._file_list = value


class SimpleDataUploader:
    def __init__(self, endpoint, data_dir):
        self.endpoint = endpoint
        self.file_list = os.listdir(data_dir)
        self.file_path_list = list(
            map(lambda x: str(pathlib.Path(data_dir).joinpath(x)), self.file_list)
        )

    def reset_default_graph_all(self):
        self.drop_default_graph(endpoint=self.endpoint)
        with alive_bar(
            len(self.file_path_list), force_tty=True, title="Uploading files"
        ) as bar:
            for file_path in self.file_path_list:
                print(pathlib.Path(file_path).name)
                self.reset_default_graph(file_path=file_path)
                bar()

    def reset_default_graph(self, file_path):
        self.upload_file(endpoint=self.endpoint, file_path=file_path)
        return True

    def upload_file(self, endpoint, file_path, format="turtle", charset="latin-1"):
        data = open(file_path).read()
        if format == "turtle":
            headers = {"Content-Type": "text/turtle"}
        elif format == "owl":
            headers = {"Content-Type": "application/rdf+xml"}

        with open(file_path, "r", encoding=charset) as file:
            data = file.read()
            r = requests.post(endpoint, data=data, headers=headers)

    def drop_default_graph(self, endpoint):
        query = "DROP DEFAULT"
        headers = {"Content-Type": "application/sparql-update"}
        r = requests.post(endpoint, data=query, headers=headers)

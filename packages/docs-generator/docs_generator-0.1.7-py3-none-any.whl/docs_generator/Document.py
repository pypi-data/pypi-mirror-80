from typing import List
from os.path import basename, sep, splitext


class Folder:
    def __init__(self, name: str):
        self.name = name
        self.files: List[Document] = []

    def add_file(self, file):
        self.files.append(file)
        return self

    def add_files(self, files):
        self.files += files
        return self

    def get_list_folder_names(self) -> List[str]:
        return self.name.split(sep)

    def __str__(self):
        return f'<Folder: {self.name}/>'

    def __repr__(self):
        return self.__str__()


class Document:
    def __init__(self, path: str):
        self.path = path

    def get_name(self):
        name = basename(self.path)
        filename, ext = splitext(name)
        filename = filename.replace('_', ' ')
        filename = filename.capitalize()
        return filename

    def get_output_name(self, ignore_name: str = ''):
        name, ext = splitext(self.path)
        return name.replace(f'{ignore_name}/', '').replace('.ipynb', '') + '.md'

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.__str__()

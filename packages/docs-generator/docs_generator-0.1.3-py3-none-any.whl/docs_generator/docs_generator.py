from yaml import dump
from .config import *
from .utils import walk_folders, generate_markdown, generate_config
from shutil import copytree


def convert_notebook_to_html(notebook_paths=None):
    """
    Convert notebooks to mkdocs html
    :param notebook_paths: notebook paths you want to have
    :return:
    """
    fs = None
    if notebook_paths:
        fs = walk_folders(notebook_paths)
    else:
        fs = walk_folders(notebook_folder)
    generate_markdown(fs)
    config = generate_config(fs)
    o = dump(config, indent=4)
    with open(config_filename, 'w') as f:
        f.write(o)

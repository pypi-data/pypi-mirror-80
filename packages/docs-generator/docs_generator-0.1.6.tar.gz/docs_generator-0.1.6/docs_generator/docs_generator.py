from yaml import dump
from .config import *
from .utils import walk_folders, generate_markdown, generate_config
from shutil import copytree


def convert_notebook_to_html(notebook_paths=None, site_name: str = "Algorithm"):
    """
    Convert notebooks to mkdocs html
    :param site_name: Site's name
    :param notebook_paths: notebook paths you want to have
    :return:
    """
    fs = None
    if notebook_paths:
        fs = walk_folders(notebook_paths)
    else:
        fs = walk_folders(notebook_folder)
    generate_markdown(fs)
    config = generate_config(fs, site_name)
    o = dump(config, indent=4)
    with open(config_filename, 'w') as f:
        f.write(o)

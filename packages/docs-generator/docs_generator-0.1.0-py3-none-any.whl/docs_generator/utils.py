from subprocess import run
from typing import List, Dict
from .config import *
from docs_generator.docs_generator.Document import Folder, Document
from docs_generator.docs_generator.config import ignore_folder
from os.path import join
import shutil
import os


def walk_folders(folder_name: str) -> List[Folder]:
    folders = []
    for dirName, subdirList, fileList in os.walk(folder_name):
        if ignore_folder not in dirName:
            if not fileList:
                continue
            new_folder_name = dirName.replace(f'{folder_name}/', '')
            folder = Folder(new_folder_name)
            new_file_list = [Document(join(dirName, f)) for f in fileList if '.ipynb' in f]
            folder.add_files(new_file_list)
            folders.append(folder)
    return folders


def generate_markdown(folders: List[Folder]):
    if os.path.exists(output_dir_name):
        shutil.rmtree(output_dir_name)
    for folder in folders:
        output_dir = os.path.join(output_dir_name, folder.name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for file in folder.files:
            run(['jupyter', 'nbconvert', f"--output-dir='{output_dir_name}'", "--to", "markdown", file.path,
                 f"--output",
                 f"{file.get_output_name(notebook_folder)}"])
            # print(file.get_output_name(notebook_folder))


def generate_config(folders: List[Folder]):
    configuration = {
        "site_name": "Algorithm",
        "nav": [],
        "theme": {"name": "material", "features": ["instant", "navigation.expand"]},
        "extra_javascript": [
            "javascripts/config.js",
            "https://polyfill.io/v3/polyfill.min.js?features=es6",
            "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js",
            "js/expand.js"
        ],
        "markdown_extensions": [
            {"pymdownx.arithmatex": {
                "generic": True
            },
            },
            {
                "pymdownx.highlight": {
                    "use_pygments": True
                }
            },
            "codehilite",
            {
                'toc': {
                    'permalink': True
                }
            }
        ]
    }
    navs = []
    for folder in folders:
        last_nav = navs[len(navs) - 1] if len(navs) > 0 else {}
        name_list = folder.get_list_folder_names()
        nav = create_object(last_nav, name_list, folder.files)
        first_key = next(iter(nav))
        first_key2 = next(iter(last_nav)) if last_nav != {} else ""
        if first_key != first_key2 or len(navs) == 0:
            navs.append(nav)
        else:
            navs[len(navs) - 1] = nav

    configuration['nav'] = navs
    return configuration


def create_object(prev_nav: Dict, name_list: List[str], files: List[Document]) -> Dict:
    """
    Generate nav object
    :param prev_nav: previous nav
    :param name_list: a list of folder's name
    :param files: a list of files
    :return: merged, navs. Created is true if the name list doesn't overlap with existing one,
    else false
    """
    name = name_list[0].capitalize()
    if len(name_list) == 1:
        new_files = [{f.get_name(): f.get_output_name(notebook_folder)} for f in files]
        if name in prev_nav:
            prev_content = prev_nav[name]
            prev_content += new_files
            prev_nav[name] = prev_content
            return prev_nav
        else:
            return {
                name: new_files
            }
    else:
        if name in prev_nav:
            prev_content = prev_nav[name]
            if isinstance(prev_content, list):
                f = create_object(prev_nav[name], name_list[1:], files)
                prev_content += [f]
            else:
                prev_content = create_object(prev_nav[name], name_list[1:], files)
            prev_nav[name] = prev_content
            return prev_nav
        else:
            data = create_object(prev_nav, name_list[1:], files)
            return {
                name: data
            }

""" Inventory is storage for generated workflows. """
import os
from pathlib import Path
import yaml
from typing import Dict, List
import shutil

import recast_workflow.workflow as workflow
from recast_workflow.definitions import *

def get_wf_path(path: str) -> str:
    """ Get path to workflow. Returns None if not found."""
    # Get end of filepath and seperate by : to see if file is not local
    path_suffix = os.path.abspath(path).rsplit('/', 1)[-1].split(':')
    if len(path_suffix) != 2: return os.path.abspath(path)

    # Add option to get workflows from non-local files
    where, name = path_suffix
    if where == 'inv':
        # Get workflow form inventory
        return get_inv_wf_path(name)
    if where == 'github':
        # TODO implement using files from github
        return

    print("{path} not found.")

def get_inv_wf_path(name: str) -> str:
    """ Return path to workflow saved in inventory. Returns None if not found."""

    # Only add .yml file suffix if not given in input name
    if not name.endswith('.yml'): name += '.yml'

    # Get name's path
    wf_path = INV_DIR / f'{name}'
    if not wf_path.exists():
        print("{name} not found in inventory.")
        return
    return wf_path

def get_inv_wf_yml(name: str, output_file='', text=False) -> Dict:
    """ Return yaml text of given workflow name """
    wf_path = get_inv_wf_path(name)
    with open(wf_path, 'r') as wf_file:
        wf_text = wf_file.read()

    if output_file:
        with open(output_file, 'w+') as out_file:
            out_file.write(wf_text)
    return wf_text if text else yaml.safe_load(wf_text)

def list_inv() -> List[str]:
    """ Returns list all workflow names in inventory """
    res = []
    for f in os.listdir(INV_DIR):
        # Make sure .yml files are not included in list (exclude __init__.py or hidden files)
        if f.endswith('.yml'):
            # Append filename without .yml suffix
            res.append(f.rsplit('/',1)[-1].rstrip('.yml'))
    return res

def remove(name: str):
    """ Remove workflow from inventory """
    wf_path = get_inv_wf_path(name)
    if not wf_path: return
    os.remove(wf_path)

def add(path: str, name='', raw_text=''):
    """ Add workflow at path to inventory """
    if raw_text:
        with open(INV_DIR / f'{name}.yml', 'w+') as wf_file:
            wf_file.write(raw_text)
        return

    if not name: name = path.rsplit('/',1)[-1]
    name = name.rstrip('.yml')
    path = os.path.abspath(path)
    shutil.copyfile(path, INV_DIR / f'{name}.yml')

def get_dir(name: str, output_path: str, reana: str = ''):
    """ Get directory with run script, inputs folder, and workflow """
    wf_path = get_inv_wf_path(name)
    if not wf_path: return

    output_path = Path(output_path)
    if output_path.exists(): output_path = output_path / name
    new_wf_path = output_path / 'workflows' / 'workflow.yml'

    # Copy template dir and modify it
    shutil.copytree(YADAGE_T_DIR, output_path)
    os.mkdir(output_path / 'workflows')
    shutil.copyfile(wf_path, new_wf_path)

    # Fill inputs.yml
    with open(output_path / 'inputs' / 'input.yml', 'w+') as inputs_file:
        inputs = {i: None for i in workflow.get_inputs({}, path=new_wf_path)}
        yaml.dump(inputs, inputs_file)

    if reana:
        reanayaml(new_wf_path, reana, output_path / 'reana.yaml')


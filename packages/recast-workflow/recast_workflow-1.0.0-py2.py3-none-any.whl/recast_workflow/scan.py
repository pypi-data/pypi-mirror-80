import os
from string import Formatter
from typing import List, Dict
import yaml

import recast_workflow.workflow as workflow

def build_multi(single_wf: dict, multi_params: List[str], name='') -> dict:
    """ Convert single stage workflow to multistage workflow given scan parameters. """
    param_arr = workflow.get_inputs(single_wf)
    params = {}

    for i in param_arr:
        params[i] = {'output': i, 'step': 'init'}
        if i in multi_params:
            params[i]['output'] = i + 's'
            params[i]['flatten'] = True

    for i in multi_params:
        if not i in params:
            print(f'Warning: multi param {i} not in workflow params.')

    multi_wf = {'stages': [{
        'dependencies': ['init'],
        'name': f'multi_{name if name else workflow.make_name(single_wf)}',
        'scheduler': {'parameters': params},
        'scheduler_type': 'multistep-stage',
        'scatter': {'method': 'zip', 'parameters': multi_params},
        'workflow' : single_wf
    }]}
    return multi_wf

def get_multi_params(tmpl_path: str):
    """ Get multiparameters from template file. """
    return [fname for _, fname, _, _ in Formatter().parse(yourstring) if fname]

def make_inputs(tmpl_path: str, output_dir_path: str, multi_params: Dict[str, List], prefix=''):
    """ Generate input files from template formatted with proper multi param values.
        multi_params is a dict that maps multi_params name to list of values. """
    tmpl_txt = ''
    with open(tmpl_path, 'r+') as tmpl_file:
        tmpl_txt = tmpl_file.read()

    output_dir_path = Path(output_dir_path)
    tmpl_name, tmpl_suffix = os.path.splitext(tmpl_path)[0]
    if not prefix: prefix = tmpl_name
    if not prefix.endswith('_'): prefix += '_'
    name_format = prefix + '_'.join(['{i}_{{{i}}}' for i in multi_params.keys()]) + tmpl_suffix

    toDo = [{k: 0 for k in multi_params.keys}]
    while len(toDo) > 0:
        # Create input file for current param combinations
        params = toDo[-1]
        for k, v in params.items(): params[k] = multi_params[k][v]

        out_filepath = name_format.format(params)
        with open(out_filepath, 'w+') as output_file:
            output_file.write(tmpl_txt.format(params))

        # Add next combinations to toDo
        for key in params.keys():
            if params[key] + 1 < len(multi_params[key]):
                toAdd = {k: v for k, v in params.items()}
                toAdd[key] += 1
                toDo.append(toAdd)

def fill_inputs(inputs_path, field, folder_path):
    """ Fills field in inputs.yml with list fo files in given folder_path. 
    Returns list of files in given folder_path."""
    allfiles = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    if inputs_path:
        with open(inputs_path, 'r+') as inputs_file:
            inputs_yml = yaml.safe_load(inputs.file.read())
        inputs_yml[field] = allfiles
        with open(inputs_path, 'w+') as inputs_file:
            inputs_file.write(yaml.dump(inputs_yml))

    return allfiles

def make_reana(wf_path, output_path):
    """ Make reana.yml for workflow at wf_path with outputs at output path."""
    with open(wf_path, 'r'):
        wf_dict = yaml.safe_load(wf_path.read())
    wf_name = wf_dict['stages'][0]['name']
    return {
            'version': '0.6.0',
            'inputs': {
                'files': ['inputs/'],
                'parameters': {'$ref: /inputs/input.yml'}
                },
            'workflow': {
                'type': 'yadage',
                'file': os.path.basename(os.path.normpath(wf_path))
                },
            'outputs': {
                'files': [output_path]
                }
            }


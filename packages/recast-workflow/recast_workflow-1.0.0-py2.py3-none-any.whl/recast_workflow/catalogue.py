import argparse
import importlib
import itertools
import logging
import os
from collections import OrderedDict, defaultdict, namedtuple
from typing import Dict, List, OrderedDict, Union

import yaml

from recast_workflow import definitions
from recast_workflow import utils

def get_all_combinations():
    """Returns all possible subworkflow combinations."""
    Pair = namedtuple('Pair', ['step', 'subworkflow'])
    pair_to_output_interfaces = defaultdict(set)
    input_interface_to_pairs = defaultdict(set)
    step_dir_paths = [
        d for d in definitions.SUBWORKFLOWS_DIR.glob('*') if d.is_dir()]
    step_to_pairs = {
        s.name: [w.name for w in s.glob('*')] for s in step_dir_paths}
    for step, subworkflows in step_to_pairs.items():
        for subworkflow in subworkflows:
            pair = Pair(step, subworkflow)
            description = utils.get_subworkflow_description(step, subworkflow)
            if len(description['interfaces']['input']) == 0:
                description['interfaces']['input'].append('none')
            if len(description['interfaces']['output']) == 0:
                description['interfaces']['output'].append('none')
            # TODO: update when interface design is decided.
            pair_to_output_interfaces[pair] = [
                description['interfaces']['output'][0]]
            for input_interface in [description['interfaces']['input'][0]]:
                input_interface_to_pairs[input_interface].add(pair)

    # NOTE: assumes that no loops are possible.
    combinations = [OrderedDict({p.step: p.subworkflow})
                    for p in input_interface_to_pairs['none']]
    final_combinations = []
    while len(combinations) != 0:
        new_combinations = []
        for combination in combinations:
            last_step = next(reversed(combination))
            last_subworkflow = combination[last_step]
            last_pair = Pair(last_step, last_subworkflow)
            for output_interface in pair_to_output_interfaces[last_pair]:
                if output_interface == 'none':
                    final_combinations.append(combination)
                    break
                for pair in input_interface_to_pairs[output_interface]:
                    new_combination = combination.copy()
                    new_combination[pair.step] = pair.subworkflow
                    new_combinations.append(new_combination)
        combinations = new_combinations

    return final_combinations


def get_valid_combinations(common_inputs: Dict[str, str]) -> List[OrderedDict[str, str]]:
    """Given values for common inputs, returns all combinations of subworkflows that support those values.
    Each common input should be defined in recast_workflow/common_inputs.yml, in which it is associated with a set of steps.
    Each subworkflow for those steps is assumed to implement a common_inputs.py file with an is_valid() -> bool function.
    This function is called for each subworkflow to determine whether it should be included.
    Once the set of allowed subworkflows for these steps is determined, the set of all possible combinations is generated using the interfaces listed in description.yml for each subworkflow.
    Args:
        common_inputs: A dict where each key-value pair is of the form (input name, input value).
    Returns:
        A list of ordered dictionaries, where each ordered dictionary has key-value pairs of the form (step, subworkflow) which describe one possible subworkflow combination that is valid for the given common inputs.
    """

    descriptions = utils.get_common_inputs(include_descriptions=True)
    invalid_inputs = set(common_inputs.keys()).difference(
        descriptions.keys())
    if invalid_inputs:
        raise ValueError(
            f'common inputs {invalid_inputs} were provided, but these are not defined in common_inputs.yml.')

    steps = set(itertools.chain.from_iterable(
        descriptions[k]['steps'] for k in common_inputs))
    allowed = {step: set() for step in steps}
    for step in steps:
        step_dir_path = utils.get_step_dir_path(step)
        subworkflow_dir_paths = [
            d for d in step_dir_path.glob('*') if d.is_dir()]
        for subworkflow_dir_path in subworkflow_dir_paths:
            common_inputs_script_path = subworkflow_dir_path / 'common_inputs.py'
            if not common_inputs_script_path.exists():
                raise RuntimeError(
                    f'Subworkflow {subworkflow_dir_path.name} for step {step} is missing common_inputs.py.')
            try:
                spec = importlib.util.spec_from_file_location(
                    'common_inputs', common_inputs_script_path)
                common_inputs_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(common_inputs_module)
                if common_inputs_module.is_valid(**{k: v for k, v in common_inputs.items() if k in common_inputs_module.is_valid.__code__.co_varnames}):
                    allowed[step].add(subworkflow_dir_path.name)
            except Exception:
                logging.error(
                    f'Subworkflow {subworkflow_dir_path.name} for step {step} has an invalid common_inputs.py.')
                raise

    combinations = get_all_combinations()
    combinations = [c for c in combinations if all(
        s not in c or c[s] in allowed[s] for s in steps)]

    return combinations


def get_missing_inputs(step: str, subworkflow_name: str, inputs: Dict[str, str], include_descriptions=False, include_optional=False) -> Union[List[str], Dict[str, str]]:
    """Returns the inputs for the given subworkflow that are missing from the given inputs."""
    description = utils.get_subworkflow_description(step, subworkflow_name)
    common_inputs = utils.get_common_inputs(step, include_descriptions)
    if include_descriptions:
        required_inputs = {e['name']: e['description']
                           for e in description['inputs'] if not e['optional'] or include_optional}
        required_inputs.update(common_inputs)
        missing_inputs = {
            k: v for k, v in required_inputs.items() if k not in inputs.keys()}
    else:
        required_inputs = [e['name'] for e in description['inputs']
                           if not e['optional'] or include_optional]
        required_inputs.extend(common_inputs)
        inputs = inputs.keys()
        missing_inputs = set(required_inputs).difference(set(inputs))
    return missing_inputs


def get_invalid_inputs(step: str, subworkflow_name: str, inputs: Dict[str, str]) -> Dict[str, str]:
    """Returns a list of the elements from the given inputs that are invalid for the given subworkflow."""
    description = utils.get_subworkflow_description(step, subworkflow_name)
    common_inputs = utils.get_common_inputs(step)
    valid_inputs = set(common_inputs).union(
        set(e['name'] for e in description['inputs']))
    invalid_inputs = {k: v for k, v in inputs.items() if k not in valid_inputs}
    return invalid_inputs


def get_environment_settings(step: str, subworkflow_name: str, include_default=False) -> Union[List[str], Dict[str, str]]:
    """Returns the possible environment settings for the given subworkflow."""
    description = utils.get_subworkflow_description(step, subworkflow_name)
    if include_default:
        if 'environment_settings' not in description:
            return {}
        else:
            return {e['name']: e['default'] for e in description['environment_settings']}
    else:
        if 'environment_settings' not in description:
            return []
        else:
            return [e['name'] for e in description['environment_settings']]

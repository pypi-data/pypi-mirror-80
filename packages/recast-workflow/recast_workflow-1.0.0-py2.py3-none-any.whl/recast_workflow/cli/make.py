"""CLI group for creating new workflows"""
import click
import yaml

from recast_workflow import catalogue
from recast_workflow import workflow
from recast_workflow import inventory
from recast_workflow import utils

@click.group(name='make')
def cli():
    """Command group for creating new workflows"""

@cli.command()
def inputs():
    """ List common inputs available for generating valid combinations. """
    params = utils.get_common_inputs(include_descriptions=True)
    fmt = '{0:20}{1:60}{2:40}'
    click.secho(fmt.format(
        'INPUT',
        'DESCRIPTION',
        'STEPS'
    ))
    for key, value in params.items():
        click.secho(
            fmt.format(
                key,
                value.get('description', 'no description'),
                str(value.get('steps', 'no steps'))
            )
        )

@cli.command()
@click.option('-n','--names', help='Comma seperated names of subworkflows in workflow.', type=str)
@click.option('-s','--steps', help='Comma seperated names of steps workflow fufills.', type=str)
@click.option('-x','--no-interact', is_flag=True, help='Run make in non-interactive mode, only using cli arguements')
@click.option('-c', '--common-inputs', help='String of comma seperated common inputs in the form KEY=VALUE,KEY1=VALUE,...', type=str)
@click.option('--view-only', is_flag=True, help='Only view combinations, do not make workflow.')
@click.option('-o','--output-path', type=click.Path(file_okay=True, resolve_path=True), help='Path to output generated workflow to.')
@click.option('-i','--save-inv', is_flag=True, help='Save made workflow to inventory.')
@click.option('-p','--print', 'print_wf', is_flag=True, help='Print workflow when done.')
def new(output_path, view_only, common_inputs, no_interact, names, steps, save_inv, print_wf):
    """ Create new workflow. """

    # User filters combinations by adding common inputs
    done_adding_ci = no_interact
    ci_used = {}

    # Parse input for common input key and value
    def add_ci(ci: str):
        cil = ci.split('=')
        if len(cil) == 2:
            ci_used[cil[0].strip()] = cil[1].strip()
        else:
            click.secho(f"Common input '{ci}' not recognized.")

    # Check if common inputs already given
    if common_inputs:
        # Convert common input str to dict
        for i in common_inputs.split(','): add_ci(i.strip())

    while not done_adding_ci:
        combos = catalogue.get_valid_combinations(ci_used)
        if len(combos) == 0: click.secho('No valid combinations for given common inputs')

        # Display all valid combinations
        for index, combo in enumerate(combos):
            click.secho('-' * 50)
            click.secho(f'Combination {index + 1}:')
            fmt = '{0:20}{1:30}'
            click.secho(fmt.format('STEP', 'NAME'))
            for k, v in combo.items(): click.secho(fmt.format(k, v))
        click.secho('-' * 50)

        # Display current common inputs
        if ci_used != {}: click.secho('Current common inputs used:')
        for k, v in ci_used.items(): click.secho(f'\t{k}={v}')
        click.secho()

        # Check to add another common input
        ci_to_add = click.prompt("Add an additional common input or enter 'done' to continue", default='done',
                show_default=False, type=str)

        # Check if user is done adding ci
        if ci_to_add.lower() == 'done':
            done_adding_ci = True
            break
        add_ci(ci_to_add)

    # TODO: Add enviroment setting selection (similiar to common input process)

    if view_only: return

    if not steps: steps = []
    if not names: names = []
    env_settings = []
    if not no_interact:
        # Pick a combination number
        workflow_index = click.prompt('Select a combination, or enter 0 to cancel', type=int) - 1
        while not -1 <= workflow_index < len(combos):
            workflow_index = click.prompt('Invalid index. Try again', type=int) - 1
        if workflow_index == -1: return

        # Split into steps and names
        for k, v in combos[workflow_index].items():
            steps.append(k)
            names.append(v)
            env_settings.append({})
    else:
        steps = [i.strip() for i in steps.split(',')]
        names = [i.strip() for i in names.split(',')]
        env_settings = [{} for i in names]

    # Run recast_workflow on inputs
    workflow_text = yaml.dump(workflow.make_workflow(steps, names, env_settings))

    # Save to inventory
    if not save_inv and not no_interact and click.confirm('Save to inventory?'): save_inv = True
    if save_inv: inventory.add('', name='-'.join(names), raw_text=workflow_text)

    # Save to file or print text
    if output_path:
        with open(output_path, 'w+') as output_file:
            output_file.write(workflow_text)

    if not print_wf and not no_interact and click.confirm('Show workflow?'): print_wf = True
    if print_wf: print(workflow_text)

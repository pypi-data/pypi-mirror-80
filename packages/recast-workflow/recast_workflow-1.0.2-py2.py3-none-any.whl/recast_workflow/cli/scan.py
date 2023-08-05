import click
import yaml

import recast_workflow.workflow as workflow
import recast_workflow.inventory as inv
import recast_workflow.scan as scan

@click.group(name='scan')
def cli():
    """ Command group for creating new scans. """

@cli.command()
@click.option('-n', '--name', type=str, help='Name of workflow in inventory')
@click.option('-f', '--filepath', type=click.Path(exists=True), help='Filepath to workflow')
@click.option('-o','--output-path', type=click.Path(file_okay=True, resolve_path=True), help='Path to output built workflow to.')
@click.option('-i', '--inv-save', is_flag=True, help='Save to inventory')
@click.argument('scanparams', type=str)
def build(name, filepath, output_path, scanparams, inv_save):
    """ Convert existing single-step workflow into multistage workflow for scans given comma-seperated scan parameters. """
    if not name and not filepath:
        click.echo('Must provide input file or name of workflow in inventory')
        return

    single_wf_yml = {}
    if filepath:
        if name: click.echo('Warning: both name and filepath passed as options, using filepath.')
        with open(filepath, 'r') as wf_file:
            single_wf_yml = yaml.safe_load(wf_file.read())
    else:
        single_wf_yml = inv.get_inv_wf_yml(name)

    multi_wf_txt = yaml.dump(scan.build_multi(single_wf_yml, scanparams.split(',')))

    if inv_save:
        inv.add('', f'multi_{workflow.make_name(single_wf_yml)}', raw_text=multi_wf_txt)
    if output_path:
        with open(output_path, 'w+') as output_file:
            output_file.write(multi_wf_txt)
    if not inv_save and not output_path:
        click.echo(multi_wf_txt)

@cli.command()
@click.option('-o','--output-path', type=click.Path(file_okay=True, resolve_path=True), help='Path to output built workflow to.')
@click.argument('template', type=click.Path(exists=True))
@click.argument('scanparams', type=str)
def getinputs(template, output_path, scanparams):
    """ Generates input files by formatting template using scanparams dict
    (eg. {param1: [value1, value2], param2: ...})."""

    if not output_path: output_path = '.'
    make_inputs(template, output_path, yaml.safe_load(scanparams))

@cli.command()
@click.argument('workflowpath', type=click.Path(exists=True))
@click.argument('dataoutpath', type=click.Path())
@click.option('-o','--output-path', type=click.Path(file_okay=True, resolve_path=True), help='Path to output reana.yml to.')
def reanayaml(workflowpath, dataoutpath, output_path):
    """ Returns reana.yml used for submitting reana jobs 
    for the given WORKFLOWPATH for which one workflow outputs to DATAOUTPATH"""
    res = make_reana(workflowpath, dataoutpath)
    if not output_path:
        print(yaml.dump(res))
        return

    with open(output_path, 'w+') as outfile:
        outfile.write(yaml.dump(res))

@cli.command()
@click.argument('inputspath', type=click.Path(exists=True))
@click.argument('field', type=str)
@click.argument('folderpath', type=(click.Path(exists=True)))
def fillinputs(inputs, field, folderpath):
    fill_inputs(inputs, field, folderpath)

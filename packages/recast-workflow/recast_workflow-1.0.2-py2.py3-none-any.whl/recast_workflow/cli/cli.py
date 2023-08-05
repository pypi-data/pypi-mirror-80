import click

from . import complete, make, inv, scan

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def recast_wf():
    """ Command-line interface for recast-workflow. """

recast_wf.add_command(complete.cli)
recast_wf.add_command(make.cli)
recast_wf.add_command(inv.cli)
recast_wf.add_command(scan.cli)


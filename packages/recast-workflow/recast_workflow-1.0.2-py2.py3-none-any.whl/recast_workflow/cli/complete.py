""" Shell completions for recast-workflow """
import click
import click_completion

click_completion.init()

@click.command(help='Generate shell completion code.', name='completions')
@click.argument(
    'shell',
    required=False,
    type=click_completion.DocumentedChoice(click_completion.core.shells),
    )
def cli(shell):
    '''Generate shell completion code for various shells.'''
    click.echo(click_completion.core.get_code(shell, prog_name='recast-wf'))

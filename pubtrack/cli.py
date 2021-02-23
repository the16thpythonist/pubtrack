import os
import pathlib

import click

PATH = pathlib.Path(__file__).parent.absolute()
VERSION_PATH = os.path.join(PATH, 'VERSION')


# HELPER FUNCTIONS
# ================

def get_version() -> str:
    with open(VERSION_PATH, mode='r') as version_file:
        # The version file is written manually by a human, which means that there is the possibility that the file
        # contains an unwanted extra whitespace or newline character. These have to be cleaned up.
        return version_file.read().replace('\n', '').replace(' ', '')


# ACTUAL CLI COMMAND IMPLEMENTATIONS
# ==================================

@click.group('pubtrack', invoke_without_command=True)
@click.option('-v', '--version', is_flag=True, short_help='Print the version string for the project')
@click.pass_context
def cli(ctx, version):
    """
    == PUBTRACK COMMAND LINE UTILITIES ==


    """
    if version:
        version = get_version()
        click.secho(version, bold=True)
        return 0


@click.command('build')
@click.argument('mode', type=click.Choice(['Production', 'local'], case_sensitive=False))
@click.pass_context
def build(ctx, mode):
    click.secho('==| BUILDING PUBTRACK CONTAINERS |==')
    click.secho(f'--| Mode: {mode}')

    return 0


if __name__ == "__main__":
    cli()

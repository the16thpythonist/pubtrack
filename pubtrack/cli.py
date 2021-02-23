import os
import pathlib
import subprocess
from typing import Tuple

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


def execute_command(command: str, verbose=True) -> Tuple[int, str]:
    click.secho(f'[*] {command}', fg='gray')
    output = subprocess.PIPE if verbose else subprocess.DEVNULL
    completed_process = subprocess.run(
        command,
        shell=True,
        stdout=output,
        stderr=output,
    )
    output = completed_process.stdout.decode()
    click.secho(output, fg='gray')

    return completed_process.returncode, output


# ACTUAL CLI COMMAND IMPLEMENTATIONS
# ==================================

@click.group('pubtrack', invoke_without_command=True)
@click.option('-v', '--version', is_flag=True, help='Print the version string for the project')
@click.pass_context
def cli(ctx, version):
    """
    == PUBTRACK COMMAND LINE UTILITIES ==


    """
    if version:
        version = get_version()
        click.secho(version, bold=True)
        return 0


@click.command('build', short_help='Build the necessary docker containers for the ')
@click.argument('mode', type=click.Choice(['Production', 'local'], case_sensitive=False))
@click.pass_context
def build(ctx, mode):
    click.secho('==| BUILDING PUBTRACK CONTAINERS |==')
    click.secho(f'--| Mode: {mode}')

    execute_command('ls -la')

    return 0


cli.add_command(build)


if __name__ == "__main__":
    cli()

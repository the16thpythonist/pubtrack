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


def execute_command(command: str, verbose: bool = True, color: str = 'cyan') -> Tuple[int, str]:
    click.secho(f'[*] {command}', fg=color)
    output = subprocess.PIPE if verbose else subprocess.DEVNULL
    completed_process = subprocess.run(
        command,
        shell=True,
        stdout=output,
        stderr=output,
    )
    output = completed_process.stdout.decode()
    click.secho(output, fg=color)

    return completed_process.returncode, output


# ACTUAL CLI COMMAND IMPLEMENTATIONS
# ==================================

@click.group('pubtrack', invoke_without_command=True)
@click.option('-v', '--version', is_flag=True, help='Print the version string for the project')
@click.option('-s', '--sudo', is_flag=True, help='Flag for using sudo status to run all docker related commands')
@click.pass_context
def cli(ctx, version, sudo):
    """
    == PUBTRACK COMMAND LINE UTILITIES ==


    """
    click.secho(str(ctx))
    ctx['sudo'] = sudo

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

    click.secho(ctx['sudo'])
    execute_command('ls -la')

    return 0


cli.add_command(build)


if __name__ == "__main__":
    cli()

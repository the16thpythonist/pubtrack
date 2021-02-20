import os
import click


@click.group('pubtrack', invoke_without_command=True)
@click.option('-v', '--version', is_flag=True)
def cli(ctx, version):

    if version:
        click.secho('0.0.0')
        return 0


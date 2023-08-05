from greble_flow.managment.manager import FlowManager

import click


@click.group()
def cli():
    pass


@cli.command()
def runprocessor():
    from web.managment import app
    app.run()

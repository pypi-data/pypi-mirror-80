from greble_flow.managment.manager import FlowManager

import click


@click.group()
def cli():
    pass


@cli.command()
@click.option("--flow_name", required=True, help="Flow name")
def runprocessor(flow_name):
    flow_manager = FlowManager()
    flow_manager.run(flow_name)

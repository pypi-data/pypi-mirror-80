import click


@click.group()
def cli():
    pass


@cli.command()
def runprocessor():
    from greble_flow.web.managment import app
    app.run()

import click


@click.command()
@click.option('--brick', default=None, type=click.Path(dir_okay=False,
                                                       exists=True))
@click.argument('image', required=True)
@click.argument('output', default=None, required=False)
def main(brick, image, output):
    pass

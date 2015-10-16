import os
import click
import legoify

@click.command()
@click.option('--brick', default=None, type=click.Path(dir_okay=False,
                                                       exists=True))
@click.argument('image', required=True)
@click.argument('output', default=None, required=False)
def main(brick, image, output):
    if not brick:
        here = os.path.abspath(os.path.dirname(__file__))
    legoify.main(image, brick=os.path.join(here, 'bricks', 'brick.png'))

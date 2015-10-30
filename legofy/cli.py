import os
import click
import legofy

@click.command()
@click.option('--brick', default=None, type=click.Path(dir_okay=False,
                                                       exists=True))
@click.option('--bricks', default=30, required=False, type=int)
@click.argument('image', required=True)
@click.argument('output', default=None, required=False)
def main(brick, image, output, bricks):
    if not brick:
        here = os.path.abspath(os.path.dirname(__file__))
        brick = os.path.join(here, 'bricks', 'brick.png')
    if not bricks : bricks = 30
    legofy.main(image, brick=brick, bricks=bricks)

if __name__ == '__main__':
    main()

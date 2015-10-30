import os
import click
import legofy

@click.command()
@click.option('--brick', default=None, type=click.Path(dir_okay=False,
                                                       exists=True))
@click.argument('image', required=True)
def main(brick, image):
    if not brick:
        here = os.path.abspath(os.path.dirname(__file__))
        brick = os.path.join(here, 'bricks', 'brick.png')
    legofy.main(image, brick=brick)

if __name__ == '__main__':
    main()
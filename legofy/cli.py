import os
import click
import legofy

@click.command()
@click.option('--brick', default=None, type=click.Path(dir_okay=False,
                                                       exists=True))
@click.option('--hd/--sd', default=False)
@click.argument('image', required=True)
@click.argument('output', default=None, required=False)
def main(brick, image, output, hd):
    if not brick:
        here = os.path.abspath(os.path.dirname(__file__))
        brick = os.path.join(here, 'bricks', 'brick.png')
    legofy.main(image, hd, brick=brick)

if __name__ == '__main__':
    main()

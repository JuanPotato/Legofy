import os
import click
import legofy

@click.command()
@click.option('--brick', default=os.path.join(os.path.dirname(__file__), "bricks", "brick.png"), type=click.Path(dir_okay=False, exists=True))
@click.option('--palette', default=os.path.join(os.path.dirname(__file__), "palettes", "legos.csv"), type=click.Path(dir_okay=False, exists=True))
@click.argument('image', required=True)
# @click.argument('output', default=None, required=False)
def main(brick, image, palette):#, output):
   legofy.main(image, brick, palette)

if __name__ == '__main__':
    main()
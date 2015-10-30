import os
import click
import legofy

@click.command()
@click.option('--brick', default=None, type=click.Path(dir_okay=False, exists=True))
@click.argument('image', required=True)
# @click.argument('output', default=None, required=False)
def main(brick, image):#, output):
    if brick:
        legofy.main(image, brick=brick)
    else:
        legofy.main(image)

if __name__ == '__main__':
    main()
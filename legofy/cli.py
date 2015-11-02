import os
import click
import legofy

@click.command()
@click.option('--brick', default=None, type=click.Path(dir_okay=False, exists=True))
@click.argument('image', required=True)
@click.argument('output', default=None, required=False)
def main(brick, image, output):
    if brick and output:
        legofy.main(image, brick=brick, output=output)
    if brick:
        legofy.main(image, brick=brick)
    if output:
        legofy.main(image, output=output)
        

if __name__ == '__main__':
    main()

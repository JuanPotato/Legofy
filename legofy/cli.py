'''Command line interface to Legofy'''
import click
import legofy


@click.command()
@click.option('--brick', default=None, type=click.Path(dir_okay=False, exists=True))
@click.argument('image', required=True)
@click.argument('output', default=None, required=False)
def main(brick, image, output):
    '''Main entry point'''
    if brick and output:
        legofy.main(image, brick=brick, output=output)
    elif brick:
        legofy.main(image, brick=brick)
    elif output:
        legofy.main(image, output=output)
    else:
        legofy.main(image)

if __name__ == '__main__':
    main()

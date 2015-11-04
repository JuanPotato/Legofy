'''Command line interface to Legofy'''
import click
import legofy


@click.command()
@click.option('--brick', default=None, type=click.Path(dir_okay=False, exists=True))
@click.argument('image', required=True)
@click.argument('scale', required=True)
@click.argument('output', default=None, required=False)
def main(image, scale, brick, output):
    '''Main entry point'''
    if brick and output:
        legofy.main(image, scale, brick=brick, output=output)
    elif brick:
        legofy.main(image, scale, brick=brick)
    elif output:
        legofy.main(image, scale, output=output)
    else:
        legofy.main(image, scale)

if __name__ == '__main__':
    main()

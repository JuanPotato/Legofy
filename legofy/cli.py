'''Command line interface to Legofy'''
import click
import legofy


@click.command()
@click.argument('image', required=True, type=click.Path(dir_okay=False, exists=True, resolve_path=True))
@click.argument('output', default=None, required=False, type=click.Path(resolve_path=True))
@click.option('--bricks', default=None, required=False, type=int)
@click.option('--brick', default=None, required=False, type=click.Path(dir_okay=False, exists=True, resolve_path=True))
def main(image, output, bricks, brick):
    '''Main entry point'''
    if output:
        if bricks:
            if brick:
                legofy.main(image, output=output, bricks=bricks, brick_path=brick)
            else:
                legofy.main(image, output=output, bricks=bricks)
        elif brick:
            legofy.main(image, output=output, brick_path=brick)
        else:
            legofy.main(image, output=output)
    elif bricks:
        if brick:
            legofy.main(image, bricks=bricks, brick_path=brick)
        else:
            legofy.main(image, bricks=bricks)
    elif brick:
        legofy.main(image, brick_path=brick)
    else:
        legofy.main(image)


if __name__ == '__main__':
    main()

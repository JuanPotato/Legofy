'''Command line interface to Legofy'''
import click
import legofy


@click.command()

@click.argument('image', required=True, type=click.Path(dir_okay=False,
                                                        exists=True,
                                                        resolve_path=True))
@click.argument('output', default=None, required=False,
                type=click.Path(resolve_path=True))
@click.option('--bricks', default=None, required=False, type=int)
@click.option('--brick', default=None, required=False,
              type=click.Path(dir_okay=False, exists=True, resolve_path=True))
@click.option('--dither/--no-dither', default=False)
@click.option('--palette', default=None, required=False,
              type=click.Choice(['mono', 'solid', 'transparent', 'effects', 'all']))
def main(image, output, bricks, brick, palette, dither):
    '''Main entry point'''
    legofy.main(image, output_path=output, bricks=bricks, brick_path=brick,
                palette_mode=palette, dither=dither)

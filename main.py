import legofy
import click

@click.command()
@click.option('--image', default='input.jpg', help='输入图片路径')
@click.option('--output', default='output.jpg', help='输出图片路径')
@click.option('--palette', default='all', help='使用的调色板')
def run_legofy(image, output, palette):
    legofy.main(image, output, palette=palette)

if __name__ == '__main__':
    run_legofy()
import legofy

here = os.path.abspath(os.path.dirname(__file__))
legofy.main("./Legofy/examples/brick.png", brick=os.path.join(here, 'bricks', 'brick.png'))
# legofy.main(image, brick=os.path.join(here, 'bricks', 'brick.png'))

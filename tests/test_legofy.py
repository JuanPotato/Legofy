import legofy
import os

here = os.path.abspath(os.path.dirname(__file__))
legofyDir = os.path.join(here, os.pardir, "legofy")
paletteDir = os.path.join(legofyDir, "palettes")
brickDir = os.path.join(legofyDir, "bricks")

# print(here)
# print(legofy)
legofy.main(os.path.join(here, 'image.jpg'), os.path.join(brickDir, 'brick.png'), os.path.join(paletteDir, 'legos.csv'))
# legofy.main(image, brick=os.path.join(here, 'bricks', 'brick.png'))

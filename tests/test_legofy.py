import legofy
import os

here = os.path.abspath(os.path.dirname(__file__))
# print(here)
# print(legofy)
legofy.main(os.path.join(here, 'image.jpg'), False, os.path.join(here, 'brick.png'))
# legofy.main(image, brick=os.path.join(here, 'bricks', 'brick.png'))

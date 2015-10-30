# coding:utf-8
import legofy
import os

here = os.path.abspath(os.path.dirname(__file__))
# print(here)
# print(legofy)
legofy.main(os.path.join(here, 'image.jpg'), os.path.join(here, 'brick.png'))
# legofy.main(image, brick=os.path.join(here, 'bricks', 'brick.png'))
legofy.main(os.path.join(here, 'bátman.png'), os.path.join(here, 'brick.png'))

import legofy
import os

brick_img = 'brick.png'
target_img = 'image.jpg'

here = os.path.abspath(os.path.dirname(__file__))
target_img_path = os.path.join(here, target_img)
brick_img_path = os.path.join(here, brick_img)

# print(here)
# print(legofy)
legofy.main(target_img_path, brick_img_path)
# legofy.main(image, brick=os.path.join(here, 'bricks', 'brick.png'))
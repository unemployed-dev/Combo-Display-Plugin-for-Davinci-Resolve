import numpy as np
from PIL import Image
import os
image_paths = os.listdir(f'{os.getcwd()}/combo_gen/images')
images =[ Image.open(f'{os.getcwd()}/combo_gen/images/{i}').convert("RGBA") for i in image_paths ]

down = Image.open(f'{os.getcwd()}/combo_gen/images - backup/ar_r.png').convert("RGBA")
# skinny_amount =20
# width, height = down.size
# left = 0 + skinny_amount/2
# top = 0
# right = width - skinny_amount/2
# bottom = height
# down = down.crop((left, top, right, bottom))
# down.save('./combo_gen/images/key-d.png')

# pick the image which is the smallest, and resize the others to match it
# min_shape = sorted( [(np.sum(i.size), i.size ) for i in images])[0][1]
# imgs_resized = [i.resize((101,101)) for i in images]
down = down.resize((101,101))
down.save('./combo_gen/images/key-d.png')


# for i,location in enumerate(image_paths):
#     print(f'saving {location}')
#     imgs_resized[i].save(location)
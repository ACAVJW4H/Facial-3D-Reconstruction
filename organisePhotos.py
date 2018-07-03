#Renames photos from cards to i.CR2

import os
from shutil import copyfile
import rawpy
import imageio

# Set number of cameras
CAM_NUM = 10

if CAM_NUM not in [9, 10]:
    print("Only 9 and 10 cameras supported.")
    exit()

PHOTOS = "../data"
CARDS = ["card{}".format(i) for i in range(1, CAM_NUM+1)]
NAMES  = ["{}.CR2".format(i) for i in range(1, 17)]

for card in CARDS:
    cardpath = os.path.join(PHOTOS,card)
    
    for i in range(1, 17):
        # rename images to card{} folders
        new_image = os.path.join(cardpath, NAMES[i])
        os.rename(os.path.join(cardpath, photos[i]), new_image)
    
        with rawpy.imread(new_image) as raw:
            rgb = raw.postprocess(gamma=(1,1), no_auto_bright=True)
        imageio.imsave(cardpath{}.format(i)+'.TIF', rgb)

        # 11th for the 10 camera setting
        # 15th for the 9  camera setting
        if CAM_NUM==9:
            if (i == 15):
                copyfile(os.path.join(cardpath, "15.tif"),
                        "{}.TIF".format(card))
        else:
            if (i == 11):
                copyfile(os.path.join(cardpath, "15.tif"),
                        "{}.TIF".format(card))

    
    print("Card {} done.".format(card))

#Renames photos from cards to i.CR2

import os
from shutil import copyfile
import rawpy
import imageio

PHOTOS = "../testdata"
CARDS = ["card{}".format(i) for i in range(1, 10)]
NAMES  = ["{}.CR2".format(i) for i in range(1, 17)]

for card in CARDS:
    cardpath = os.path.join(PHOTOS,card)
    
    for i in range(1, 17):
        # move images to card{} folders
        os.rename(os.path.join(cardpath, photos[i]),
                os.path.join(cardpath, NAMES[i]))

        # move 11th capture to main folder for Photoscan
        if (i == 11):
            copyfile(os.path.join(cardpath, NAMES[i]),
                     "card{}.CR2".format(card))
        
        # convert CR2 to TIFF
        raw = rawpy.imread(os.path.join(cardpath, NAMES[i-1]))
        rgb = raw.postprocess()
        imageio.imsave(os.path.join(cardpath, "{}.TIFF".format(i)), rgb)

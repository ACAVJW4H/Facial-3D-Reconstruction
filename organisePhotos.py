#Renames photos from cards to i.CR2

import os
from shutil import copyfile
import rawpy
import imageio

PHOTOS = "../testdata"
CARDS = ["card{}".format(i) for i in range(1, 11)]
NAMES  = ["{}.CR2".format(i) for i in range(1, 17)]

for card in CARDS:
    cardpath = os.path.join(PHOTOS,card)
    
    for i in range(1, 17):
        # rename images to card{} folders
        # os.rename(os.path.join(cardpath, photos[i]),
        #        os.path.join(cardpath, NAMES[i]))
    
        # move 15th capture to main folder for Photoscan
        if (i == 11):
            copyfile(os.path.join(cardpath, "11.tif"),
                     "{}.tif".format(card))
    
    print("Card {} done.".format(card))

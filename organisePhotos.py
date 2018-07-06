#Renames photos from cards to i.CR2

import os
from shutil import copyfile
import rawpy
import imageio
from PIL import Image
from shutil import copyfile

# Set number of cameras
CAM_NUM = 9

if CAM_NUM==9:
    stereoInput = 15
elif CAM_NUM==10:
    stereoInput = 11
else:
    print("Only 9 and 10 cameras supported.")
    exit()

PHOTOS = "../data"
CARDS = ["card{}".format(i) for i in range(1, CAM_NUM+1)]
NAMES  = ["{}.CR2".format(i) for i in range(1, 17)]

def new_name(dirPhotos, i):
    '''
    Find the number of the first capture in the sequence
    and renames the ith photo in the 1-16.CR2 order.
    '''

    base = int(dirPhotos[0].split(".")[0].split("_")[1])
    new  = int(dirPhotos[i].split(".")[0].split("_")[1])
    
    return str(new-base+1)+".CR2"

for card in CARDS:

    cardpath = os.path.join(PHOTOS,card)
    dirPhotos = os.listdir(cardpath)
    
    # for i in range(1, 17):
        # rename images to card{} folders
    #     new_image = new_name(dirPhotos, i-1)
    #     os.rename(os.path.join(cardpath, dirPhotos[i-1]),
    #             os.path.join(cardpath, new_image))
    
    # os.system('ubuntu run ufraw-batch --out-type tiff --gamma=1.0 ../data/{}/*.CR2'.format(card))

    copyfile(os.path.join(cardpath, "{}.tif".format(stereoInput)),
            os.path.join(PHOTOS, str(card)+".tif"))

    # remove raw
    # for image in os.listdir(cardpath):
    #     if "CR2" in image:
    #         os.remove(os.path.join(cardpath, image))
    
    print("Card {} done.".format(card))

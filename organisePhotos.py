#Renames photos from cards to i.CR2

import os
from shutil import copyfile
import rawpy
import imageio
from PIL import Image
from shutil import copyfile
import sys
import warnings
from progress.bar import Bar

# Set number of cameras
CAM_NUM = 9

# Set other constants
PHOTOS = "../data"
CARDS = ["card{}".format(i) for i in range(1, CAM_NUM+1)]
NAMES  = ["{}.tif".format(i) for i in range(1, 17)]

if CAM_NUM==9:
    STEREO_INPUT = 15
elif CAM_NUM==10:
    STEREO_INPUT = 11
else:
    print("Only 9 and 10 cameras supported.")
    exit()

# imageio throws multiple warnings that do not affect functionality
if not sys.warnoptions:
    warnings.simplefilter("ignore")

def new_name(dirPhotos, i):
    '''
    Find the number of the first capture in the sequence
    and renames the ith photo in the 1-16.CR2 order.
    '''

    base = int(dirPhotos[0].split(".")[0].split("_")[1])
    new  = int(dirPhotos[i].split(".")[0].split("_")[1])
    
    return str(new-base+1)+".CR2"

def convert_photo_linear_gamma(cardpath):
    '''
    Convert photos with linear gamma
    to be placed as card*/1-16.tif 
    and to be used for the specular and diffuse normal maps.
    '''
    rawPhotos = [raw for raw in os.listdir(cardpath)]
    # for every raw photo
    for i in range(0, 16):
        rawPath = os.path.join(cardpath, rawPhotos[i])
        rgbPath = os.path.join(cardpath, NAMES[i])

        with rawpy.imread(rawPath) as raw:
            rgb = raw.postprocess(gamma=(1,1), no_auto_bright=True, output_bps=8)
        imageio.imsave(rgbPath, rgb)

def convert_photo_bright(card):
    '''
    Convert photos with higher exposure
    to be placed as card1-9.tif
    and to be used for the specular and diffuse normal maps.
    '''
    rawPhoto = str(STEREO_INPUT) + ".CR2"
    cardpath = os.path.join(PHOTOS, card)

    rawPath = os.path.join(cardpath, rawPhoto)
    rgbPath = os.path.join(PHOTOS, card+".tif")

    with rawpy.imread(rawPath) as raw:
        rgb = raw.postprocess(use_auto_wb=True, no_auto_bright=False, output_bps=8)
    imageio.imsave(rgbPath, rgb)

def rename_photos(cardpath):
    '''
    Rename raw photos in a card folder
    to 1-16.CR2, according their place in the shooting sequence.
    '''
    dirPhotos = os.listdir(cardpath)
    for i in range(0, 16):

        new_image = new_name(dirPhotos, i)

        old_name_dir = os.path.join(cardpath, dirPhotos[i])
        new_name_dir = os.path.join(cardpath, new_image)

        os.rename(old_name_dir, new_name_dir)

def organise_raw_photos():
    '''
    Rename raw photos to match the capturing sequence,
    and convert them for normal maps and stereo reconstruction.
    '''
    bar = Bar("Organising " + str(CAM_NUM) + " cards", max=CAM_NUM)
    for card in CARDS:

        # get directories
        cardpath = os.path.join(PHOTOS,card)

        # rename
        rename_photos(cardpath)

        # convert and organise photos for maps
        convert_photo_linear_gamma(cardpath)

        # convert and organise photos for stereo
        convert_photo_bright(card)
    
        bar.next()
    bar.finish()

organise_raw_photos()
# print("Press any key to delete raw. Press 'n' or Ctrl+C to cancel.")
# inp = raw_input()

# # remove raw
# if (inp == "n"): exit()
# for card in CARDS:
#     for image in os.listdir(cardpath):
#         if "CR2" in image:
#             os.remove(os.path.join(cardpath, image))
#     print("Raw {} deleted.".format(card))

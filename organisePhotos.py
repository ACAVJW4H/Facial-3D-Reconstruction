#Renames photos from cards to i.CR2

import os
from shutil import copyfile
import numpy as np
import rawpy
import imageio
from PIL import Image
from shutil import copyfile
import sys
import warnings
from progress.bar import Bar

# Set number of cameras
CAM_NUM = 9
PHOTO_NUM = 10

# Set other constants
PHOTOS = "../data"
CARDS = ["card{}".format(i) for i in range(1, CAM_NUM+1)]
NAMES  = ["{}.tif".format(i) for i in range(1, PHOTO_NUM+1)]

# Set variables of color correction, to catch the white block
STARTHEIGHT = 2676 # Upper left pixel
STARTWIDTH  = 2205 # Upper left pixel
DISTANCE    = 130  # Travel (pixels) to lower right pixel

if CAM_NUM==9:
    STEREO_INPUT = 9
elif CAM_NUM==10:
    STEREO_INPUT = 11
else:
    print("Only 9 and 10 cameras supported.")
    exit()

RED_CORRECTION = 0.9 / 0.57508159
GREEN_CORRECTION = 0.9 / 0.33863589
BLUE_CORRECTION = 0.9 / 0.30628449
# PHOTOS = "../comp_c_grad"

# RED_CORRECTION = 0.9 / 0.68484205
# GREEN_CORRECTION = 0.9 / 0.38325126
# BLUE_CORRECTION = 0.9 / 0.11427009
# PHOTOS = "../comp_c_bin/"

# imageio throws multiple warnings that do not affect functionality
if not sys.warnoptions:
    warnings.simplefilter("ignore")

def save_np_image(im, name):
    '''
    Saves an input np.array type image as a uint8.
    '''
    im = Image.fromarray(im.astype('uint8'))
    im.save(name)

def get_white_balance_correction_values(startHeight = STARTHEIGHT, startWidth = STARTWIDTH, distance = DISTANCE):
    '''
    Use the white box in the cross-pollarized fully iluminated capture
    to find an average correction measure for automatic white balance.
    @author Mingqian
    '''
    colorChart = np.array(Image.open("../dataColors/card4/15.tif")).astype("float64")
    sum = np.array([0.,0.,0.])
    test = colorChart[startHeight : startHeight+distance, startWidth : startWidth + distance, ...]
    save_np_image(test, "../test.tif")
    #average value of a 200x200 patch
    for h in range(startHeight, startHeight + distance):
        for w in range(startWidth, startWidth + distance):
            sum[0] += colorChart[h,w,0]
            sum[1] += colorChart[h,w,1]
            sum[2] += colorChart[h,w,2]
    sum = sum / (float(distance) * float(distance) * 255.)

    print(sum)

# 0.90^3 is the greish white as appears on the camera with correct white balance
# The other three values come from get_white_balance_correction_values().
# Replace when needed.

def get_white_balance_image(im, kR = RED_CORRECTION, kG = GREEN_CORRECTION, kB = BLUE_CORRECTION):
    '''
    For an image input as a numpy array,
    it corrects the white balance according the correction values found by get_white_balance_correction_values()
    @author Mingqian
    '''

    balancedR = kR * im[...,0]
    balancedG = kG * im[...,1]
    balancedB = kB * im[...,2]

    balancedIm = np.empty_like(im).astype("float64")

    balancedIm[...,0] = balancedR
    balancedIm[...,1] = balancedG
    balancedIm[...,2] = balancedB

    return np.clip(balancedIm,0,255)

def get_raw_photos(cardpath):
    '''
    Returns a list with the directories of raw photos in the card folder.
    '''
    allPhotos = os.listdir(cardpath)
    rawPhotos = []
    
    for photo in allPhotos:
        if ".CR2" in photo:
            rawPhotos.append(photo)

    return sorted(rawPhotos)

def new_name(dirPhotos, i):
    '''
    Find the number of the first capture in the sequence
    and renames the ith photo in the 1-10.CR2 order.
    '''

    base = int(dirPhotos[0].split(".")[0].split("_")[1])
    new  = int(dirPhotos[i].split(".")[0].split("_")[1])
    
    return str(new-base+1)+".CR2"


def convert_photo_linear_gamma(cardpath):
    '''
    Convert photos with linear gamma
    to be placed as card*/1-10.tif 
    and to be used for the specular and diffuse normal maps.
    '''
    rawPhotos = get_raw_photos(cardpath)

    # for every raw photo
    for i in range(0, len(rawPhotos)):
        rawPath = os.path.join(cardpath, rawPhotos[i])
        rgbPath = os.path.join(cardpath, NAMES[i])

        if os.path.isfile(rgbPath):
            print("Skipping " + rgbPath)
        else:
            # Convert Image to tif with linear gamma
            with rawpy.imread(rawPath) as raw:
                rgb = raw.postprocess(use_auto_wb=False, gamma=(1,1), no_auto_bright=True, output_bps=8)
            imageio.imsave(rgbPath, rgb)

            # Correct white balance
            with Image.open(rgbPath) as inputImage:
                unbalancedImage = np.array(inputImage).astype("float64")
            balancedImage = get_white_balance_image(unbalancedImage)
            save_np_image(balancedImage, rgbPath)

def convert_photo_bright(card):
    '''
    Convert photos with higher exposure
    to be placed as card1-9.tif
    and to be used for the specular and diffuse normal maps.
    '''
    cardpath = os.path.join(PHOTOS, card)
    rawPhoto = get_raw_photos(cardpath)[STEREO_INPUT-1]

    rawPath = os.path.join(cardpath, rawPhoto)
    rgbPath = os.path.join(PHOTOS, card+".tif")

    if os.path.isfile(rgbPath):
        print("Skipping " + rgbPath)
    else:
        # Convert Image to tif without linear gamma
        with rawpy.imread(rawPath) as raw:
            rgb = raw.postprocess(use_auto_wb=False, no_auto_bright=True, output_bps=8)
        imageio.imsave(rgbPath, rgb)

        with Image.open(rgbPath) as inputImage:
            unbalancedImage = np.array(inputImage).astype("float64")
        balancedImage = get_white_balance_image(unbalancedImage)
        save_np_image(balancedImage, rgbPath)

def whiteBalanceImage(im,RED_CORRECTION,GREEN_CORRECTION,BLUE_CORRECTION):
    balancedR = RED_CORRECTION * im[...,0]
    balancedG = GREEN_CORRECTION * im[...,1]
    balancedB = BLUE_CORRECTION * im[...,2]
    balancedIm = np.empty_like(im).astype("float64")
    balancedIm[...,0] = balancedR
    balancedIm[...,1] = balancedG
    balancedIm[...,2] = balancedB
    return np.clip(balancedIm,0,255)

def rename_photos(cardpath):
    '''
    Rename raw photos in a card folder
    to 1-10.CR2, according their place in the shooting sequence.
    '''
    rawPhotos = get_raw_photos(cardpath)

    for i in range(0, len(rawPhotos)):

        if "IMG" in rawPhotos[i]:
            new_image = new_name(rawPhotos, i)

            old_name_dir = os.path.join(cardpath, rawPhotos[i])
            new_name_dir = os.path.join(cardpath, new_image)

            os.rename(old_name_dir, new_name_dir)

        else:
            print("Skipping Renaming in " + cardpath)
            

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
        # rename_photos(cardpath)

        # convert and organise photos for maps
        convert_photo_linear_gamma(cardpath)

        # convert and organise photos for stereo
        convert_photo_bright(card)
    
        bar.next()
    bar.finish()

# get_white_balance_correction_values()
organise_raw_photos()
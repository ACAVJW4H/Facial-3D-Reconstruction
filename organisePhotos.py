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
import pickle
from argparse import ArgumentParser

# Set number of cameras
CAM_NUM = 9
VALUES_DIR = "./white_balancing_values.pkl"

parser = ArgumentParser()
parser.add_argument("-o", "--operation", default="organise", help="if given, get white balance values for that capture")
parser.add_argument("-x", "--x", help="Upper left X of white square")
parser.add_argument("-y", "--y", help="Upper left Y of white square")
parser.add_argument("-d", "--distance", default=100, help="Distance accross the white square")
parser.add_argument("-p", "--photos", default="data", help="photos dir")
args = parser.parse_args()

# Set other constants
PHOTOS = "../{}".format(args.photos)
CARDS = ["card{}".format(i) for i in range(1, CAM_NUM+1)]
NAMES  = ["{}.tif".format(i) for i in range(1, 11)]

RED_CORRECTION = 1.
GREEN_CORRECTION = 1.
BLUE_CORRECTION = 1.

if CAM_NUM==9:
    STEREO_INPUT = 9 #15
elif CAM_NUM==10:
    STEREO_INPUT = 11
else:
    print("Only 9 and 10 cameras supported.")
    exit()

# imageio throws multiple warnings that do not affect functionality
if not sys.warnoptions:
    warnings.simplefilter("ignore")

def prepare_imagelist():
    '''
    Imagelist file for Reality Capture.
    '''
    images = ["card{}.tif\n".format(i + 1) for i in range(CAM_NUM)]
    images000 = ["0000{}.png\n".format(i) for i in range(CAM_NUM)]
    imglistName = "rawimagelist.imagelist"
    img000Name = "image000list.txt"
    with open(os.path.join(PHOTOS,imglistName), "w") as imagelist:
        imagelist.writelines(images)
    with open(os.path.join(PHOTOS,img000Name), "w") as imagelist:
        imagelist.writelines(images000)

    print("imagelist prepared")


def save_np_image(im, name):
    '''
    Saves an input np.array type image as a uint8.
    '''
    im = Image.fromarray(im.astype('uint8'))
    im.save(name)

def get_white_balance_correction_values(chartdir, startWidth, startHeight, distance):
    '''
    Use the white box in the cross-pollarized fully iluminated capture
    to find an average correction measure for automatic white balance.
    @author Mingqian
    '''
    
    wb_photo = get_raw_photos("../{}/card4".format(chartdir))[-2]
    wb_photo_tif = wb_photo.split(".CR2")[0] + ".tif"

    with rawpy.imread("../{}/card4/{}".format(chartdir, wb_photo)) as raw:
        rgb = raw.postprocess(use_auto_wb=False, gamma=(1,1), no_auto_bright=True, output_bps=8)
    imageio.imsave("../{}/card4/{}".format(chartdir, wb_photo_tif), rgb)

    colorChart = np.array(Image.open("../{}/card4/{}".format(chartdir, wb_photo_tif))).astype("float64")

    # test = colorChart
    # test[startHeight : startHeight+distance, startWidth : startWidth + distance, ...] = [245., 0., 0.]
    test = colorChart[startHeight : startHeight+distance, startWidth : startWidth + distance, ...]

    save_np_image(test, "test.tif")
 
    sum = np.array([0.,0.,0.])
    #average value of a 200x200 patch
    for h in range(startHeight, startHeight + distance):
        for w in range(startWidth, startWidth + distance):
            sum[0] += colorChart[h,w,0]
            sum[1] += colorChart[h,w,1]
            sum[2] += colorChart[h,w,2]

    sum = sum / (float(distance) * float(distance) * 255.)
    sum = 0.9 / sum
    save_np_image(get_white_balance_image(test, sum[0], sum[1], sum[2]), "testwb.tif")
    print(sum)

    with open(VALUES_DIR, 'wb') as values_file:
        pickle.dump(sum, values_file)

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
    if not os.path.isdir(os.path.join(PHOTOS, "captures")):
        os.makedirs(os.path.join(PHOTOS, "captures"))
    cardpath = os.path.join(PHOTOS, card)
    rawPhoto = get_raw_photos(cardpath)[STEREO_INPUT-1]

    rawPath = os.path.join(cardpath, rawPhoto)
    rgbPath = os.path.join(PHOTOS, os.path.join("captures/", card+".tif"))

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
    to 1-16.CR2, according their place in the shooting sequence.
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

if args.operation == "organise":
    with open(VALUES_DIR, 'rb') as values_file:
        RED_CORRECTION, GREEN_CORRECTION, BLUE_CORRECTION = pickle.load(values_file)
    organise_raw_photos()
    prepare_imagelist()
else:
    get_white_balance_correction_values(args.operation, int(args.x), int(args.y), int(args.distance))

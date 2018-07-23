'''
Import photos from the Light Stage cameras,
by loading each SD card and downloading a number of 16-photo shootings.
'''

import os
import win32api
import random
import string
import subprocess

from argparse import ArgumentParser
from progress.bar import Bar
from shutil import copy2

# Define the sequence of expressions for the folder to be named respectively
EXPRESSIONS = [
    'disgusted',
    'angry',
    'sad',
    'happy',
    'plain'
]

def print_card_info(i):
    '''
    Prints prompt for new card 
    and waits for a key to start transfering
    '''

    print("Transfer {}: Please insert next card and press any key.".format(i+1))
    print("If you wish to stop, type 's' or Ctrl+C")
    inp = raw_input()

    if (inp == "s"): exit()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    '''
    Generate random name for shooting
    '''
    return ''.join(random.choice(chars) for _ in range(size))

def get_card_name():
    ### Complete
    '''
    Gets the loaded card name and number, 
    to be used in the folder structed of the inputs.
    '''
    cardname = win32api.GetVolumeInformation("G:\\")[0]
    return cardname.lower()

def get_photo_names():
    '''
    Gets the photo names and returns a list with them sorted
    by date last modified.
    The last should be the most recent.
    '''
    photo_folders = os.listdir("G:\\DCIM")
    photos = []
    for folder in photo_folders:

        if "CANON" in folder:
            folder_path = os.path.join("G:\\DCIM", folder)
            photos_temp = sorted(os.listdir(folder_path))

            for photo in photos_temp:
                if(".CR2" in photo):
                    photos.append(os.path.join(folder_path, photo))

            dirs = subprocess.Popen(["dir", folder_path], stdout=subprocess.PIPE)
            out_dirs = dirs.stdout.read()

            # Print last items windows see
            print(out_dirs[-300:])

    # Print last item python sees, to check for occasionally missing data
    print(photos[-1].split("\\")[-1])

    if (len(photos) > 1000):
        print("---------------------------")
        print("WARNING: CARD GETTING FULL!")
        print("---------------------------")
        
    return photos

def gen_folder_names():
    '''
    Generate new folders for the shooting
    and return their directories as list
    '''

    folders = []
    for i in range(int(args.shootings)):
        folders.append(args.name + "_" + EXPRESSIONS[i])

    base_dir = "..\\"
    folder_dirs = [os.path.join(base_dir, folder)
                    for folder in folders]
    
    for folder_dir in folder_dirs:
        if not os.path.exists(folder_dir):
            os.makedirs(folder_dir)
    
    return folder_dirs

def make_transfer(card, folder_dir, photos):
    '''
    Make the transfer of one card and one shooting.
    '''
    bar = Bar("Transfering from "+card, max=16)

    folder_card = os.path.join(folder_dir, card)
    if not os.path.exists(folder_card):
        os.makedirs(folder_card)

    for photo in photos:
        # shutil.copy2 instead of copy because it copies metadata as well
        copy2(photo, folder_card)
        bar.next()

    bar.finish()


# Arguments
parser = ArgumentParser()
parser.add_argument("-s", "--shootings", default=1, help="number of shootings to be downloaded")
parser.add_argument("-n", "--name", default=id_generator(), help="folder name for the shooting")
args = parser.parse_args()

# Run for 9 cards
for i in range(9):

    print_card_info(i)
    card        = get_card_name()
    photos      = list(reversed(get_photo_names()))
    folder_dirs = gen_folder_names()
    for i in range(int(args.shootings)):
        make_transfer(
            card,
            folder_dirs[i],
            photos[16 * i : 16 * (i + 1)]
        )

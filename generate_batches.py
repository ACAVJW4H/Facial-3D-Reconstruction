import os
from argparse import ArgumentParser

DIR = "../"
EXP = [
    'plain',
    'happy',
    'sad',
    'angry',
    'disgusted',
    'fear',
    'surprised'
]

COM = "CALL {}\n"
BATCH_FILE = "batching_autoGen"

parser = ArgumentParser()
parser.add_argument("-s", "--start", default=1, help="ID from which to start batching")
args = parser.parse_args()



def get_data_folders(dir=DIR):
    "Get a set of folders for batching"

    folders = os.listdir(dir)
    captures = []

    for f in folders:
        if f.split("_")[0].isdigit() and f.split("_")[1] in EXP:
            if int(f.split("_")) >= args.start:
                captures.append(f)

    return set(sorted(captures))

def gen_coms(captures):
    "Generate batching commands for captures"

    coms = [COM.format(capture) for capture in captures]
    return coms

def write_coms(coms):
    "write a BATCH file with the coms"

    with open(BATCH_FILE+"_{}.bat".format(args.start), "w") as batchfile:
        batchfile.writelines(coms)
    
    print(BATCH_FILE+"_{}.bat exported.".format(args.start))

write_coms(gen_coms(get_data_folders()))

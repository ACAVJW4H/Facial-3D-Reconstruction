import os
from argparse import ArgumentParser

EXPRESSIONS = [
    '_plain',
    '_happy',
    '_sad',
    '_angry',
    '_disgusted'
]

FILES = [
    '_LQ.obj',
    '_HQ.obj',
    '.zip'
]

global name_counter

def get_size(filename):
    file_stats = os.stat(filename)
    return file_stats.st_size

def update_counter():
    global name_counter
    name_counter = str(int(name_counter) + 1)

def get_files_to_rename():

    basedir = os.getcwd()

    all_files = os.listdir(basedir)
    files_to_rename = []

    # files with name contain dashes in the date
    for file_name in all_files:
        if "-" in file_name and ".zip" in file_name:
            files_to_rename.append(
                file_name.split("_")[0]
                + "_" +
                file_name.split("_")[1]
            )

    return files_to_rename

def rename_file(src, dest):
    '''
    Rename a single file and check it was successful.
    '''

    if (os.path.exists(src)):

        size_before = get_size(src)

        assert(not os.path.exists(dest))
        os.rename(src, dest)

        size_after = get_size(dest)
        assert(size_before == size_after)

    else:
        print(src + " does not exist.")

    print(dest + " renamed.")

def rename_all(files_to_rename):

    cwd = os.getcwd()

    for base_name in files_to_rename:
        for expression in EXPRESSIONS:

            src_base = os.path.join(cwd, base_name)
            src_base_exp = src_base + expression
            
            dest_base = os.path.join(cwd, name_counter)
            dest_base_exp = dest_base + expression

            for file_name in FILES:
                src = src_base_exp + file_name
                dest = dest_base_exp + file_name
                rename_file(src, dest)

        update_counter()


parser = ArgumentParser()
parser.add_argument("-n", "--starting_number", required=True, help="The number name to start")
args = parser.parse_args()

name_counter = args.starting_number

files_to_rename = get_files_to_rename()
rename_all(files_to_rename)

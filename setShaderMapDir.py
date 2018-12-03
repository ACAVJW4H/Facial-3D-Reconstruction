from argparse import ArgumentParser
import os

SCRIPTS_DIR = "./"
SHADERMAP_SCRIPT = "shadermap.lua"

parser = ArgumentParser()
parser.add_argument("-p", "--path", default="data", help="give a path for the photo folder")
args = parser.parse_args()

with open(os.path.join(SCRIPTS_DIR, SHADERMAP_SCRIPT), "r") as luafile:
    luascript = luafile.read()

luascript = luascript.replace("F:\\\\LS_dataset\\\\data\\\\", "F:\\\\LS_dataset\\\\{}\\\\".format(args.path))

with open(os.path.join(SCRIPTS_DIR, SHADERMAP_SCRIPT), "w") as luafile:
    luafile.write(luascript)
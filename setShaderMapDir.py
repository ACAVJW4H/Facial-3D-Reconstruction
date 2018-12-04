from argparse import ArgumentParser
import os

SCRIPTS_DIR = "./"
SHADERMAP_SCRIPT = "shadermap.lua"
BLENDER_SCRIPT = "blenderScript.mlx"

parser = ArgumentParser()
parser.add_argument("-p", "--path", default="data", help="give a path for the photo folder")
args = parser.parse_args()

def replaceValue(script, origin, target):
    with open(os.path.join(SCRIPTS_DIR, script), "r") as scriptfile:
        luascript = scriptfile.read()

    luascript = luascript.replace(origin, target)

    with open(os.path.join(SCRIPTS_DIR, script), "w") as scriptfile:
        scriptfile.write(luascript)

replaceValue(SHADERMAP_SCRIPT,
    "F:\\\\LS_dataset\\\\data\\\\",
    "F:\\\\LS_dataset\\\\{}\\\\".format(args.path)
)

replaceValue(SHADERMAP_SCRIPT,
    "blenderTexture",
    "{}_texture".format(args.path)
)

replaceValue(BLENDER_SCRIPT,
    "blenderTexture.png",
    "{}_texture.png".format(args.path)
)
import PIL
from PIL import Image
from PIL import ImageFilter
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-p", "--path", default="data", help="give a path for the photo folder")
args = parser.parse_args()

# Set other constants
data = "../{}".format(args.path)

specular = Image.open("{}/blenderTexture.png".format(data))
blurredSpecular = specular.filter(PIL.ImageFilter.GaussianBlur(radius=1))

blurredSpecular.save("{}/blenderTexture.png".format(data), "PNG")
import PIL
from PIL import Image
from PIL import ImageFilter
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-p", "--path", default="data", help="give a path for the photo folder")
args = parser.parse_args()

# Set other constants
data = "../{}".format(args.path)

specular = Image.open("{}/{}_texture.png".format(data, args.path))
blurredSpecular = specular.filter(PIL.ImageFilter.MedianFilter(9))

blurredSpecular.save("{}/{}_texture.png".format(data, args.path), "PNG")
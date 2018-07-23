import PIL
from PIL import Image
from PIL import ImageFilter

specular = Image.open("../data/result.png")
blurredSpecular = specular.filter(PIL.ImageFilter.GaussianBlur(radius=2))

blurredSpecular.save("../data/result.png", "PNG")
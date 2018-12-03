"""
Generate a Meshlab MLP projet (mlp) with the registered images and the reconstructed model,
as produced by Reality Capture and exported as Bundler .OUT, Wavefront .OBJ and Camera params .CSV.
It is necessary as meshlabserver cannot currently read .OUT files.
@author Alexander Lattas, Imperial College London 
"""

from argparse import ArgumentParser
from PIL import Image
import csv
import os

parser = ArgumentParser()
parser.add_argument("-p", "--path", default="data", help="set the project folder")
args = parser.parse_args()

DATA_DIR = "../{}".format(args.path)
OUTPUT_FILENAME = "{}/meshlab.mlp".format(DATA_DIR)
IMAGE_LIST = "{}/image000list.txt".format(DATA_DIR)
PROJECT_FILE = "{}/cameras.csv".format(DATA_DIR)
BUNDLER_FILE = "{}/bundler.out".format(DATA_DIR)

HEAD = """
<!DOCTYPE MeshLabDocument>
<MeshLabProject>
 <MeshGroup>
  <MLMesh label="model" filename="RCExport.obj">
   <MLMatrix44>
    1 0 0 0
    0 1 0 0
    0 0 1 0
    0 0 0 1
   </MLMatrix44>
  </MLMesh>
 </MeshGroup>
 <RasterGroup>
"""

END = """
 </RasterGroup>
</MeshLabProject>
"""

MLRasterStart = """
  <MLRaster label="{}">
"""

MLRasterEnd = """
  </MLRaster>
"""

VCGCamera = """
   <VCGCamera PixelSizeMm="1 1" LensDistortion="0 0" ViewportPx="{} {}" 
   TranslationVector="{} {} {} 1" CameraType="0" 
   RotationMatrix="{} {} {} 0 {} {} {} 0 {} {} {} 0 0 0 0 1 " 
   CenterPx="{} {}" FocalMm="{}"/>
"""

Plane = """
   <Plane semantic="1" fileName="{}"/>
"""

# Both Plane and MLRaster get one argument, the picture filename, including the extension
# VCG Camera takes the following:

class Camera:
    def __init__(self, name):
        self.name = name
    
    # Setters
    def setViewPortPx(self, xy):
        x, y = xy
        self.ViewportPx = [int(x), int(y)]
        self.CenterPx = [int(int(x)/2), int(int(y)/2)]
    
    def setCameraCoords(self, coords):
        x, y, z = coords
        self.TranslationVector = [-x, -y, -z]
    
    def setRotationMatrix(self, rotationMatrix):
        self.RotationMatrix = rotationMatrix
    
    def setFocalMm(self, focalMm):
        self.FocalMm = [float(focalMm)]

    # Calculations
    def getValues(self):
        """
        Create a list with all the values for the VCGCamera field
        """
        self.values = tuple(
            self.ViewportPx +
            self.TranslationVector +
            self.RotationMatrix +
            self.CenterPx +
            self.FocalMm
        )
        return self.values


def getCameraNames(image_list_dit):
    "Get camera names from the imagelist file"
    with open(image_list_dit, "r") as imagelistfile:
        imagelist = imagelistfile.readlines()
        imagelist = [image.strip("\n") for image in imagelist]
    return imagelist


def getViewportPx(name):
    """
    Get the camera's capture dimensions (viewportpx)
    """
    im = Image.open(os.path.join(DATA_DIR, name))
    width, height = im.size
    return width, height


def getCameraPosition(name):
    """
    Get the camera positions from the RC project csv.
    """
    with open(PROJECT_FILE, 'rb') as f:
        reader = csv.reader(f)
        cameras = list(reader)
    cam_num = int(name.split(".")[0][-1]) + 1
    xyz = cameras[cam_num][1:4]
    x, y, z = float(xyz[0]), float(xyz[1]), float(xyz[2])
    return [x, y, z]


def getFocalAndRotation(bunlder_file):
    """
    Disect the beginning of the bundler file to get
    - The number of cameras registered (2nd line, 1st num)
    - The FocalMm Value (1st line/camera, 1st num)
    - The Rotation Matrix (next 3 lines/camera)
    """
    with open(bunlder_file, 'r') as bundler_file:
        bundler = bundler_file.readlines()

    cam_num = int(bundler[1].split(" ")[0])
    focal_list = []
    rot_list = []

    for cam in range(cam_num):
        focal_list.append(
            # Each camera has 5 lines of data, and first 2 bundler lines are skipped.
            float(bundler[2 + (5 * cam)].split(" ")[0])
        )
        rot_list.append(
            # Skip two first lines, and read [1:4] of each camera's lines,
            # each line has 3/9 items and put the all in one list   
            [
                float(bundler[3 + row + (5 * cam)].split(" ")[item])
                for row in range(3) 
                for item in range(3)
            ]
        )

    return cam_num, focal_list, rot_list


def getCamerasList(camera_names):
    """
    Get a list of Camera objects and find their values
    """
    cameras = [Camera(name) for name in camera_names]
    cam_num, focal_list, rot_list = getFocalAndRotation(BUNDLER_FILE)

    for i in range(cam_num):
        cameras[i].setViewPortPx(getViewportPx(cameras[i].name)[:])
        cameras[i].setCameraCoords(getCameraPosition(cameras[i].name))
        cameras[i].setFocalMm(focal_list[i])
        cameras[i].setRotationMatrix(rot_list[i])

    return cameras


def writeMeshlabProject(output_filename, cameras_list):
    """
    Write the MLP project file.
    """
    with open(output_filename, "w") as mlpfile:
        mlpfile.writelines([HEAD])
        for camera in cameras_list:
            mlpfile.writelines([MLRasterStart.format(camera.name)])
            
            mlpfile.writelines([VCGCamera.format(*camera.getValues())])

            mlpfile.writelines([Plane.format(camera.name)])
            mlpfile.writelines([MLRasterEnd])
        mlpfile.writelines([END])


def main():
    camera_names = getCameraNames(IMAGE_LIST)
    cameras_list = getCamerasList(camera_names)
    writeMeshlabProject(OUTPUT_FILENAME, cameras_list)

if __name__ == "__main__":
    main()

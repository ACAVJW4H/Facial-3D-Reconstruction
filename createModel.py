import PhotoScan
import os

# Set number of cameras
CAM_NUM = 9

if CAM_NUM not in [9, 10]:
    print("Only 9 and 10 cameras supported.")
    exit()

PhotoScan.gpu_mask = 1  #GPU devices binary mask
PhotoScan.cpu_enable = True

path = os.path.dirname(os.path.abspath(__file__)) + "/../data/"

def createAndSaveModel():
    doc = PhotoScan.app.document
    chunk = doc.addChunk()

    photos = []

    for i in range(1, CAM_NUM+1):
        photos.append(path + "card{}.tif".format(i))

    print(photos)

    chunk.addPhotos(photos)

    # align cameras, first pass
    for frame in chunk.frames:
        frame.matchPhotos(accuracy=PhotoScan.HighAccuracy)
    chunk.alignCameras()

    # align all unaligned cameras not done in first pass
    for camera in doc.chunk.cameras:
        if not camera.transform:
            doc.chunk.alignCameras([camera])

    chunk.optimizeCameras(adaptive_fitting=True)

    chunk.buildDepthMaps(quality = PhotoScan.UltraQuality, filter = PhotoScan.AggressiveFiltering)
    chunk.buildDenseCloud()
    chunk.buildModel(
        surface = PhotoScan.Arbitrary, 
        interpolation = PhotoScan.EnabledInterpolation, 
        face_count = PhotoScan.FaceCount.MediumFaceCount, 
        source = PhotoScan.DataSource.DenseCloudData)
    chunk.smoothModel(4)

    # For meshlab project file
    chunk.exportCameras("{}bundler.out".format(path), PhotoScan.CamerasFormat.CamerasFormatBundler)
    chunk.exportCameras("{}agisoftXML.xml".format(path), PhotoScan.CamerasFormat.CamerasFormatXML)
    chunk.exportCameras("{}blocksExchange.xml".format(path), PhotoScan.CamerasFormat.CamerasFormatBlocksExchange)
    # The actual model
    chunk.exportModel("{}agisoftExport.obj".format(path), format=PhotoScan.ModelFormat.ModelFormatOBJ)

    # doc.save(path=path+filename, chunks= [doc.chunk])


if __name__ == "__main__":
    createAndSaveModel()

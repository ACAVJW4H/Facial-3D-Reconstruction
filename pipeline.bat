@echo off
REM @author Alexander Lattas
REM alexandros.lattas17@imperial.ac.uk
REM Project on github.com/lattas/facial-3d-reconstruction
REM Reconstructs a 3D model of a face using pictures of different illumination and angle, as taken by a light stage.
REM Based on Mridul Kumar's MEng thesis project
REM ---
REM Create Model
REM ---
REM Set Paths
SET pathToAgisoft="C:\Program Files\Agisoft\PhotoScan Pro"
SET pathToMeshLab="..\meshlab"
SET pathToBlender="C:\Program Files\Blender Foundation\Blender"
REM Begin
REM ---
REM Reconstruct 3D Model with Photoscan Agisoft
REM The fully illuminated, cross-pollarized photos should be in createModel.py's directory, names card{}.JPG
REM %pathToAgisoft%\photoscan.exe -r createModel.py
REM ECHO 3D MODEL RECONSTRUCTED
REM Compute diffuse and specular Normal Maps
REM Photos should be in ..\data\card{}\1-16.TIF
python photometricNormals.py --maps
ECHO DIFFUSE AND SPECULAR MAPS COMPUTED
REM Compose Meshlab diffuse project,
REM execute the blenderScript to create the texture map from the diffuse normals and
REM connect their coordinates with the model.
python photometricNormals.py --diffuseProj
%pathToMeshLab%\meshlabserver.exe -p specularProject.mlp -i agisoftExport.obj -s blenderScript.mlx -w forBlender.mlp
ECHO MESHLAB DIFFUSE PROJECT EXECUTED
REM Compose Meshlab specular project,
REM execute the blenderScript to create the texture map from the specular normals and
REM connect their coordinates with the model.
python photometricNormals.py --specularProj
%pathToMeshLab%\meshlabserver.exe -p specularProject.mlp -i agisoftExport_out.obj -s blenderScript.mlx -w specularAdded.mlp
ECHO MESHLAB SPECULAR PROJECT EXECUTED
REM Apply Gaussian blur of radius 1
python blur.py
ECHO BLUR APPLIED.
ECHO CONVERT SPECULAR MAP TO DISPLACEMENT MAP WITH SHADER MAP 4 AND PRESS A KEY.
REM Before continuing, the specular normal texture map should be imported to Shader Map 4
REM and converted by hand to a displacement map with height 100 and contrast 108-112.
REM The result should overwrite the input file with the same name in same location.
REM ---
REM Execute the blender script to create detail on the model using the texture map.
%pathToBlender%\blender.exe -b -P blender.py
ECHO BLENDER SCRIPT EXECUTED.

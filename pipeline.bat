@echo off
REM @author Alexander Lattas
REM alexandros.lattas17@imperial.ac.uk
REM Project on github.com/lattas/facial-3d-reconstruction
REM Reconstructs a 3D model of a face using pictures of different illumination and angle, as taken by a light stage.
REM Based on Mridul Kumar's MEng thesis project
REM ------------------Paths---------------------
REM Set Paths to external Applications
SET Photoscan="C:\Program Files\Agisoft\PhotoScan Pro\photoscan.exe"
SET Meshlab="..\meshlab\meshlabserver.exe"
SET Blender="C:\Program Files\Blender Foundation\Blender\blender.exe"
SET ShaderMap4="C:\Program Files\ShaderMap 4\bin\ShaderMap.exe"
REM Begin
REM --------------Reconstruction----------------
REM Reconstruct 3D Model with Photoscan Agisoft
REM The fully illuminated, cross-pollarized photos should be in createModel.py's directory, names card{}.JPG
ECHO STARTING: 3D model reconstruction with Agisoft Photoscan
%Photoscan% -r createModel.py
ECHO DONE:     3D model reconstruction as agisoftExport.obj
REM ------------------Normals-------------------
REM Compute diffuse and specular Normal Maps
REM Photos should be in ..\data\card{}\1-16.TIF
ECHO STARTING: Computing diffuse and specular normal maps
python photometricNormals.py --maps
ECHO DONE:     Diffuse and specular normal maps
REM ---------------diffuseProject---------------
REM Compose Meshlab diffuse project,
REM execute the blenderScript to create the texture map from the diffuse normals and
REM connect their coordinates with the model.
ECHO STARTING: Executing diffuseProject with meshlab
python photometricNormals.py --diffuseProj
%Meshlab% -p ..\data\diffuseProject.mlp -i ..\data\agisoftExport.obj -s blenderScript.mlx -w ..\data\diffuseAdded.mlp
ECHO DONE:     Meshlab diffuseProject 
REM --------------specularProject---------------
REM Compose Meshlab specular project,
REM execute the blenderScript to create the texture map from the specular normals and
REM connect their coordinates with the model.
ECHO STARTING: Executing specularProject with meshlab
python photometricNormals.py --specularProj
%Meshlab% -p ..\data\specularProject.mlp -i ..\data\agisoftExport_out.obj -s blenderScript.mlx -w ..\data\specularAdded.mlp
MOVE blenderTexture.png ..\data\blenderTexture.png
COPY ..\data\blenderTexture.png ..\data\blenderTextureBKP.png
ECHO DONE:     Meshlab specularProject and blenderTexture
REM --------------------Blur---------------------
REM Apply Gaussian blur of radius 1
ECHO STARTING: Applying blur on blenderTexture
python blur.py
ECHO DONE:     blur applyed on blenderTexture
REM --------------DisplacementMap-----------------
REM The blenderTexture specular normal map is converted
REM to a displacement map with ShaderMap 4, overwriting the input.
ECHO STARTING: Computing displacement map with ShaderMap
%ShaderMap4% shadermap.lua
ECHO DONE:     Displacement map computed as blenderTexture
REM -----------------Subdivision------------------
REM The displacement map is used, along with its coordinates on the model,
REM as embedded by meshlab, to do a subdivision on it, to create details such as pores and wrinkles.
ECHO STARTED: Subdividing AgisoftExport with Blender
%blender% -b -P blender.py
ECHO DONE:    Final model produced as final.obj

@echo off
REM @author Alexander Lattas
REM alexandros.lattas17@imperial.ac.uk
REM Project on github.com/lattas/facial-3d-reconstruction
REM Reconstructs a 3D model of a face using pictures of different illumination and angle, as taken by a light stage.
REM Based on Mridul Kumar's MEng thesis project
REM ------------------Paths---------------------
REM Set Paths to external Applications
SET Photoscan="D:\software\agisoft\photoscan.exe"
SET Meshlab="D:\software\meshlab2018\distrib\meshlabserver.exe"
SET Blender="C:\Program Files\Blender Foundation\Blender\blender.exe"
SET ShaderMap4="C:\Program Files\ShaderMap 4\bin\ShaderMap.exe"
SET SevenZip="C:\Program Files\7-Zip\7z.exe"
REM Begin
REM ------------------Name----------------------
REM Rename the folder in the arguments to 
REM ECHO STARTED: Renaming Folder
SET FolderName=%1
ECHO Reconstructing %FolderName%...
REN ..\%FolderName% data
REM ECHO DONE:    Renamed Folder
REM --------------Convert Photos----------------
REM ECHO STARTED: Preprocessing photos
REM python organisePhotos.py
REM ECHO DONE: Photos converted to TIFF
REM --------------Reconstruction----------------
REM Reconstruct 3D Model with Photoscan Agisoft
REM The fully illuminated, cross-pollarized photos should be in createModel.py's directory, names card{}.JPG
REM ECHO STARTING: 3D model reconstruction with Agisoft Photoscan
REM %Photoscan% -r createModel.py
REM ECHO DONE:     3D model reconstruction as agisoftExport.obj
REM REM ------------------Normals-------------------
REM Compute diffuse and specular Normal Maps
REM Photos should be in ..\data\card{}\1-16.TIF
REM ECHO STARTING: Computing diffuse and specular normal maps
REM python photometricNormalsShort.py
REM ECHO DONE:     Diffuse and specular normal maps
REM ---------------diffuseProject---------------
REM Compose Meshlab diffuse project,
REM execute the blenderScript to create the texture map from the diffuse normals and
REM connect their coordinates with the model.
REM ECHO STARTING: Executing diffuseProject with meshlab
REM python photometricNormals.py --diffuseProj
REM %Meshlab% -p ..\data\diffuseProject.mlp -i ..\data\agisoftExport.obj -s blenderScript.mlx -w ..\data\diffuseAdded.mlp
REM ECHO DONE:     Meshlab diffuseProject 
REM --------------specularProject---------------
REM Compose Meshlab specular project,
REM execute the blenderScript to create the texture map from the specular normals and
REM connect their coordinates with the model.
MOVE ..\data\agisoftExport_out.obj ..\data\agisoftExport_out.BACKUP.obj
COPY ..\data\%FolderName%_LQ.obj ..\data\agisoftExport_out.obj
ECHO STARTING: Executing specularProject with meshlab
python photometricNormals.py --specularProj
%Meshlab% -p ..\data\specularProject.mlp -i ..\data\agisoftExport_out.obj -s blenderScript.mlx -w ..\data\specularAdded.mlp
MOVE blenderTexture.png ..\data\blenderTexture.png
REM COPY ..\data\blenderTexture.png ..\data\blenderTextureBKP.png
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
REM -------------------Export---------------------
REM Copy LQ and HQ models out of folder
REM COPY ..\data\agisoftExport.obj ..\%FolderName%_LQ.obj
REM COPY ..\data\final.obj ..\%FolderName%_HQ.obj
COPY ..\data\final.obj ..\results\%FolderName%_HQ.obj
REM REM Zip (quickly) the whole project and rename it back to original name
REM ECHO STARDED: Compressing project folder
REN ..\data %FolderName%
REM %SevenZip% a -tzip ..\%FolderName%.zip ../%FolderName%/* -mx1
REM ECHO DONE:    Project folder compressed
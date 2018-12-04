@echo off
REM @author Alexander Lattas
REM alexandros.lattas17@imperial.ac.uk
REM Project on github.com/lattas/facial-3d-reconstruction
REM Reconstructs a 3D model of a face using pictures of different illumination and angle, as taken by a light stage.


REM ------------------Paths---------------------
REM Set Paths to external Applications
SET Photoscan="D:\software\agisoft\photoscan.exe"
SET Meshlab="D:\software\meshlab2018\distrib\meshlabserver.exe"
SET Blender="C:\Program Files\Blender Foundation\Blender\blender.exe"
SET ShaderMap4="C:\Program Files\ShaderMap 4\bin\ShaderMap.exe"
SET SevenZip="C:\Program Files\7-Zip\7z.exe"
SET NICPDir="F:\GAN-Lightstage"
SET ScriptDir="F:\LS_Dataset\facial-3d-reconstruction"

REM ------------------Name----------------------
REM Get Data Folder as an argument to this script
SET FolderName=%1

REM CALL conda activate lightstage
REM --------------Convert Photos----------------
ECHO STARTED: Preprocessing photos
REM python organisePhotos.py -p %FolderName%
ECHO DONE: Photos converted to TIFF

REM --------------Reconstruction----------------
REM Reconstruct 3D Model with Capturing Reality and replace normals with photos
ECHO STARTING: 3D model reconstruction with Reality Capture
REM createModelRC.bat %FolderName% "reconstruct"
ECHO DONE:     3D model reconstruction as RCExport.obj

REM ------------------Normals--------------------
REM Compute diffuse and specular Normal Maps
ECHO STARTING: Computing diffuse and specular normal maps
REM python photometricNormalsShort.py -p %FolderName%
REM createModelRC.bat %FolderName% "specularRegistration"
ECHO DONE:     Diffuse and specular normal maps

REM --------------Meshlab Project---------------
ECHO STARTING: Generating Meshlab Project for Texture parametarisation
REM COPY blenderScriptBackUp.mlx blenderScript.mlx
REM python generateMeshlabProj.py -p %FolderName%
ECHO DONE:     Meshlab project exported as meshlab.mlp

REM CD %NICPDir%
CALL conda activate menpo3

REM -------------Registration-------------------
ECHO STARTING: Template registration to the reconstructed model
REM python %NICPDir%\large_scale_NICP_UV_Formulation.py -p %FolderName%

REM CD %ScriptDir%

REM ----------Texture Parametarisation----------
ECHO STARTING: Parametarisation of normals on the RCExport.obj
REM COPY shadermapBackUp.lua shadermap.lua 
REM python setShaderMapDir.py -p %FolderName%
REM %Meshlab% -p ..\%FolderName%\meshlab.mlp -i ..\%FolderName%\%FolderName%_LQ.obj -s blenderScript.mlx -w ..\%FolderName%\parametarised.mlp
REM MOVE %FolderName%_texture.png ..\%FolderName%\.
REM COPY ..\%FolderName%\%FolderName%_texture.png ..\%FolderName%\Normals.png
ECHO DONE:     Meshlab specularProject and blenderTexture

REM --------------DisplacementMap-----------------
REM The blenderTexture specular normal map is converted
REM to a displacement map with ShaderMap 4, overwriting the input.
REM ECHO STARTING: Computing displacement map with ShaderMap
REM %ShaderMap4% shadermap.lua 
REM COPY shadermapBackUp.lua shadermap.lua 
REM ECHO DONE:     Displacement map computed as blenderTexture

REM --------------------Blur---------------------
REM Apply Gaussian blur of radius 1
REM ECHO STARTING: Applying blur on blenderTexture
REM python blur.py -p %FolderName%
ECHO DONE:     Blur applyed on blenderTexture

REM -----------------Subdivision------------------
REM The displacement map is used, along with its coordinates on the model,
REM as embedded by meshlab, to do a subdivision on it, to create details such as pores and wrinkles.
REM ECHO STARTED: Subdividing AgisoftExport with Blender
REM %blender% -b -P blender.py -- data
REM ECHO DONE:    Final model produced as final.obj

REM ----------------HQ Texture--------------------
REM createModelRC.bat %FolderName% "textureRegistration"
REM %Meshlab% -p ..\%FolderName%\meshlab.mlp -i ..\%FolderName%\%FolderName%_HQ.obj -s blenderScript.mlx -w ..\%FolderName%\parametarised.mlp
REM MOVE %FolderName%_texture.png ..\%FolderName%\.
REM COPY ..\%FolderName%\00*.png ..\%FolderName%\captures\.
REM COPY blenderScriptBackUp.mlx blenderScript.mlx

REM REM -------------Orientation-------------------
ECHO STARTING: Template registration to the reconstructed model
python %NICPDir%\large_scale_NICP_UV_Formulation.py -l -p %FolderName%

REM -------------------Export---------------------
REM Copy LQ and HQ models out of folder
REM COPY ..\%FolderName%\RCExport.obj ..\results\%FolderName%_LQ.obj
REM COPY ..\%FolderName%\final.obj ..\results\%FolderName%_HQ.obj
REM REM Zip (quickly) the whole project and rename it back to original name
ECHO STARDED: Compressing project folder
REM %SevenZip% a -tzip ..\%FolderName%.zip ../%FolderName%/* -mx1
REM ECHO DONE:    Project folder compressed
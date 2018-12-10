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
SET Mode=%2

CALL conda activate lightstage
REM --------------Convert Photos----------------
ECHO STARTED: Preprocessing photos
python organisePhotos.py -p %FolderName%
ECHO DONE: Photos converted to TIFF

REM --------------Reconstruction----------------
REM REM Reconstruct 3D Model with Capturing Reality and replace normals with photos
ECHO STARTING: 3D model reconstruction with Reality Capture
CALL createModelRC.bat %FolderName% "reconstruct"
MKDIR ..\%FolderName%\capturesRegistered\.
COPY ..\%FolderName%\00*.png ..\%FolderName%\capturesRegistered\.
ECHO DONE:     3D model reconstruction as RCExport.obj

------------------Normals--------------------
Compute diffuse and specular Normal Maps
ECHO STARTING: Computing diffuse and specular normal maps
python photometricNormalsShort.py -p %FolderName%
CALL createModelRC.bat %FolderName% "specularRegistration"
ECHO DONE:     Diffuse and specular normal maps
echo %Mode%
REM --------------Meshlab Project---------------
ECHO STARTING: Generating Meshlab Project for Texture parametarisation
COPY blenderScriptBackUp.mlx blenderScript.mlx
python generateMeshlabProj.py -p %FolderName%
REM ECHO DONE:     Meshlab project exported as meshlab.mlp

IF %Mode%==NoRegistration (
    COPY ..\%FolderName%\RCExport.obj ..\%FolderName%\%FolderName%_LQ.obj
) ELSE (
    CD %NICPDir%
    CALL conda activate menpo3
    REM -------------Registration-------------------
    ECHO STARTING: Template registration to the reconstructed model
    python %NICPDir%\large_scale_NICP_UV_Formulation.py -p %FolderName% -t "full_33k"

    CD %ScriptDir%
)

REM ----------Texture Parametarisation----------
ECHO STARTING: Parametarisation of normals on the RCExport.obj
COPY shadermapBackUp.lua shadermap.lua 
python setShaderMapDir.py -p %FolderName%
%Meshlab% -p ..\%FolderName%\meshlab.mlp -i ..\%FolderName%\%FolderName%_LQ.obj -s blenderScript.mlx -w ..\%FolderName%\parametarised.mlp
MOVE %FolderName%_texture.png ..\%FolderName%\.
COPY ..\%FolderName%\%FolderName%_texture.png ..\%FolderName%\Normals.png
ECHO DONE:     Meshlab specularProject and blenderTexture

REM --------------DisplacementMap-----------------
REM The blenderTexture specular normal map is converted
REM to a displacement map with ShaderMap 4, overwriting the input.
ECHO STARTING: Computing displacement map with ShaderMap
python setShaderMapDir.py -p %FolderName%
%ShaderMap4% shadermap.lua 
COPY shadermapBackUp.lua shadermap.lua 
ECHO DONE:     Displacement map computed as blenderTexture

REM --------------------Blur---------------------
REM Apply Gaussian blur of radius 1
ECHO STARTING: Applying blur on blenderTexture
python blur.py -p %FolderName%
ECHO DONE:     Blur applyed on blenderTexture

REM -----------------Subdivision------------------
REM The displacement map is used, along with its coordinates on the model,
REM as embedded by meshlab, to do a subdivision on it, to create details such as pores and wrinkles.
ECHO STARTED: Subdividing AgisoftExport with Blender
%blender% -b -P blender.py -- %FolderName%
ECHO DONE:    Final model produced as final.obj

REM ----------------HQ Texture--------------------
CALL createModelRC.bat %FolderName% "textureRegistration"
%Meshlab% -p ..\%FolderName%\meshlab.mlp -i ..\%FolderName%\%FolderName%_HQ.obj -s blenderScript.mlx -w ..\%FolderName%\parametarised.mlp
%Meshlab% -p ..\%FolderName%\meshlab.mlp -i ..\%FolderName%\%FolderName%_LQ.obj -s blenderScript.mlx -w ..\%FolderName%\parametarised.mlp
MOVE %FolderName%_texture.png ..\%FolderName%\%FolderName%_texture.png 
COPY blenderScriptBackUp.mlx blenderScript.mlx
DEL ..\%FolderName%\%FolderName%_HQ_out.obj
DEL ..\%FolderName%\%FolderName%_HQ_out.obj.mtl
MOVE ..\%FolderName%\%FolderName%_LQ_out.obj ..\%FolderName%\%FolderName%_LQ.obj

IF %Mode%==NoRegistration (
    echo No Orientation change
) ELSE (
    REM REM -------------Orientation-------------------
    REM ECHO STARTING: Template registration to the reconstructed model
    python %NICPDir%\large_scale_NICP_UV_Formulation.py -l -p %FolderName%
)

REM -------------------Export---------------------
REM Copy LQ and HQ models out of folder
REM COPY ..\%FolderName%\RCExport.obj ..\results\%FolderName%_LQ.obj
REM COPY ..\%FolderName%\final.obj ..\results\%FolderName%_HQ.obj
REM REM Zip (quickly) the whole project and rename it back to original name
ECHO STARDED: Compressing project folder
REM %SevenZip% a -tzip ..\%FolderName%.zip ../%FolderName%/* -mx1
REM ECHO DONE:    Project folder compressed
@echo off 
REM Command Line Execution of Reality Capture
REM for creating a 3D reconstruction of Light Stage pictures
REM and exporting the mesh and bundler so as to be loaded by Meshlab
REM Author: Alexander Lattas of iBug Imperial College London and Facesoft

REM ------ Settings ------
set dataRelativeDir=%1
set dataAbsDir="F:\LS_dataset\%dataRelativeDir%"
set settingsdir="F:\LS_dataset\facial-3d-reconstruction\RCSettings"
set RC="C:\Program Files\Capturing Reality\RealityCapture\RealityCapture.exe"

REM -exportXmp uses current settins, which are set to locked.

REM --- Reconstruction ---
%RC% -newScene -add %dataAbsDir%\imagelist.imagelist ^
    -align ^
    -exportRegistration %settingsdir%\RegistrationExport.xml %dataAbsDir%\bundler.out ^
    -exportRegistrationUndistoredImages %settingsdir%\RegistrationExport.xml %dataAbsDir% ^
    -exportXmp ^
    -setReconstructionRegion %settingsdir%\reconstructionRegionBig.rcbox ^
    -mvs -calculateVertexColors ^
    -set "smoothIterations=10" -set "smoothWeight=0.8" -set "mvsFltSmoothingStyle=0" -set "mvsFltSmoothingType=1" ^
    -closeHoles -clean -simplify 300000 -smooth ^
    -exportModel "Model 5" %dataAbsDir%\RCExport.obj %settingsdir%\ModelExport.xml ^
    -save %dataAbsDir%\RCProject.rcproj ^
-quit


REM --- Specs Registration ---
DEL %dataAbsDir%\card*.tif
COPY %dataAbsDir%\speca\card*.tif %dataAbsDir%\.

%RC% -load %dataAbsDir%\RCProject.rcproj ^
    -exportRegistrationUndistoredImages %settingsdir%\RegistrationExport.xml %dataAbsDir% ^
-quit

DEL %dataAbsDir%\card*.tif
COPY %dataAbsDir%\ims\card*.tif %dataAbsDir%\.

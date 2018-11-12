@echo off 
REM Command Line Execution of Reality Capture
REM for creating a 3D reconstruction of Light Stage pictures
REM and exporting the mesh and bundler so as to be loaded by Meshlab
REM Author: Alexander Lattas of iBug Imperial College London and Facesoft

REM ------ Settings ------
set dataRelativeDir=%1
set dataAbsDir="F:\LS_dataset\%dataRelativeDir%"
set settingsdir="F:\LS_dataset\facial-3d-reconstruction\RCSettings"
REM set scriptDir = "F:\LS_dataset\facial-3d-reconstruction"
set RC="C:\Program Files\Capturing Reality\RealityCapture\RealityCapture.exe"

REM --- Reconstruction ---
%RC% -newScene -add %dataAbsDir%\imagelist.imagelist ^
    -align ^
    -exportRegistration %settingsdir%\RegistrationExport.xml %dataAbsDir%\bundler.out ^
    -setReconstructionRegion %settingsdir%\reconstructionRegionBig.rcbox ^
    -mvs -calculateVertexColors ^
    -set "smoothIterations=10" -set "smoothWeight=0.8" -set "mvsFltSmoothingStyle=0" -set "mvsFltSmoothingType=1" ^
    -closeHoles -clean -simplify 300000 -smooth ^
    -exportModel "Model 5" %dataAbsDir%\RCExport.obj %settingsdir%\ModelExport.xml ^
    -save %dataAbsDir%\RCProject.rcproj ^
-quit

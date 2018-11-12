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

REM In Application Settings: (cant import them yet through code)
REM Smoothing: Type:Strong, Weight:0.5, Iterations: 8

REM --- Reconstruction ---
%RC% -newScene -add %dataAbsDir%\imagelist.imagelist ^
    -align ^
    -exportRegistration %settingsdir%\RegistrationExport.xml %dataAbsDir%\bundler.out ^
    -setReconstructionRegionAuto -mvs -calculateVertexColors ^
    -clean -simplify 300000 -smooth ^
    -exportModel "Model 4" %dataAbsDir%\RCExport.obj %settingsdir%\ModelExport.xml ^
    -save %dataAbsDir%\RCProject.rcproj ^
-quit
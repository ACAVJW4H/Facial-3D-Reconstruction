@echo off 
REM Command Line Execution of Reality Capture
REM for creating a 3D reconstruction of Light Stage pictures
REM and exporting the mesh and bundler so as to be loaded by Meshlab
REM Author: Alexander Lattas of iBug Imperial College London and Facesoft

REM ------ Settings ------
set dataRelativeDir=%1
set mode=%2
echo %mode%
set dataAbsDir="F:\LS_dataset\%dataRelativeDir%"
set settingsdir="F:\LS_dataset\facial-3d-reconstruction\RCSettings"
set RC="C:\Program Files\Capturing Reality\RealityCapture\RealityCapture.exe"

REM MKDIR %dataAbsDir%\speculars
REM MKDIR %dataAbsDir%\capturesBKP

REM -exportXmp uses current settins, which are set to locked.

REM --- Reconstruction ---
if %mode%=="reconstruct" (
    %RC% -newScene -addFolder %dataAbsDir%\captures\ ^
        -align ^
        -exportRegistration %settingsdir%\RegistrationExportOUT.xml %dataAbsDir%\bundler.out ^
        -exportRegistration %settingsdir%\RegistrationExportCSV.xml %dataAbsDir%\cameras.csv ^
        -exportRegistrationUndistoredImages %settingsdir%\RegistrationExportOUT.xml %dataAbsDir% ^
        -exportXmp ^
        -setReconstructionRegion %settingsdir%\reconstructionRegionBig.rcbox ^
        -mvs -calculateVertexColors ^
        -set "smoothIterations=7" -set "smoothWeight=0.7" -set "mvsFltSmoothingStyle=0" -set "mvsFltSmoothingType=1" ^
        -closeHoles -clean -simplify 300000 -smooth ^
        -exportModel "Model 5" %dataAbsDir%\RCExport.obj %settingsdir%\ModelExport.xml ^
        -save %dataAbsDir%\RCProject.rcproj ^
    -quit
)

if %mode%=="specularRegistration" (
    MKDIR %dataAbsDir%\capturesBKP
    MOVE %dataAbsDir%\captures\*.tif %dataAbsDir%\capturesBKP\.
    COPY %dataAbsDir%\speculars\*.tif %dataAbsDir%\captures\.

    %RC% -load %dataAbsDir%\RCProject.rcproj ^
        -exportRegistrationUndistoredImages %settingsdir%\RegistrationExportOUT.xml %dataAbsDir% ^
    -quit

    MOVE %dataAbsDir%\capturesBKP\*.tif %dataAbsDir%\captures\.
)

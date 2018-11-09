@echo off 
REM Command Line Execution of Reality Capture
REM for creating a 3D reconstruction of Light Stage pictures
REM and exporting the mesh and bundler so as to be loaded by Meshlab
REM Author: Alexander Lattas of iBug Imperial College London and Facesoft

REM ------ Settings ------
set dataRelativeDir=%1
set dataAbsDir="F:/LS_dataset/%dataRelativeDir%"
set RC="C:/Program Files/Capturing Reality/RealityCapture/RealityCapture.exe"

REM --- Reconstruction ---
%RC% -newScene -quit
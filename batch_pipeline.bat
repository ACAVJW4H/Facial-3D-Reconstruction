@echo off
REM @author Alexander Lattas
REM alexandros.lattas17@imperial.ac.uk
REM Project on github.com/lattas/facial-3d-reconstruction
REM Reconstructs a 3D model of a face using pictures of different illumination and angle, as taken by a light stage.
REM This script runs the reconstruction pipeline for multiple objects.
REM HOW: give the date_name of the folders as an argument
REM --------------Run Pipelines--------------
CALL pipeline.bat %folderName%_plain
CALL pipeline.bat %folderName%_happy
CALL pipeline.bat %folderName%_sad
CALL pipeline.bat %folderName%_angry
CALL pipeline.bat %folderName%_disgusted
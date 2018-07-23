@echo off
REM @author Alexander Lattas
REM alexandros.lattas17@imperial.ac.uk
REM Project on github.com/lattas/facial-3d-reconstruction
REM Reconstructs a 3D model of a face using pictures of different illumination and angle, as taken by a light stage.
REM This script runs the reconstruction pipeline for multiple objects.
REM HOW: give the date_name of the folders as an argument
REM -------------Get Folder Names------------
SET folderName=%1
SET plain=%folderName%_plain
SET happy=%folderName%_happy
SET sad=%folderName%_sad
SET angry=%folderName%_angry
SET disgusted=%folderName%_disgusted
--------------Run Pipelines--------------
pipeline.bat %plain%
pipeline.bat %happy%
pipeline.bat %sad%
pipeline.bat %angry%
pipeline.bat %disgusted%
REM ---------Send Completion Email----------
REM Set objMail = CreateObject("CDO.Message")
REM Set objConf = CreateObject("CDO.Configuration")
REM Set objFlds = objConf.Fields
REM objFlds.Item("http://schemas.microsoft.com/cdo/configuration/sendusing") = 2
REM objFlds.Item("http://schemas.microsoft.com/cdo/configuration/smtpserver") = "123-140.iphost.gr"
REM objFlds.Item("http://schemas.microsoft.com/cdo/configuration/smtpserverport") = 465
REM objFlds.Item("http://schemas.microsoft.com/cdo/configuration/sendusername") = "lightstage@lattas.eu"
REM objFlds.Item("http://schemas.microsoft.com/cdo/configuration/sendpassword") = "light_stage"
REM objFlds.Item("http://schemas.microsoft.com/cdo/configuration/smtpauthenticate") = 1
REM objFlds.Update
REM objMail.Configuration = objConf
REM objMail.FromName = "Graphic27 @ Lighstage"
REM objMail.From = "lightstage@lattas.eu"
REM objMail.To = "alexander@lattas.eu"
REM objMail.Subject = "Project Completed:"
REM objMail.TextBody = %folderName%
REM objMail.Send
REM Set objFlds = Nothing
REM Set objConf = Nothing
REM Set objMail = Nothing
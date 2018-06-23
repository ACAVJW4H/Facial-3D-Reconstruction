SET pathToScript=%cd%
SET pathToAgisoft="C:\Program Files\Agisoft\PhotoScan Pro"
CD %pathToAgisoft%
photoscan.exe -r %pathToScript%\createModel.py
CD %pathToScript%
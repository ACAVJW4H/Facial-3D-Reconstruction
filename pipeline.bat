REM Create Model
REM ---
SET testing="yes"
SET testingnext="yes"
SET pathToScript=%cd%
SET pathToAgisoft="C:\Program Files\Agisoft\PhotoScan Pro"
CD %pathToAgisoft%
photoscan.exe -r %pathToScript%\createModel.py
CD %pathToScript%
REM ---
SET pathToMeshLab="..\meshlab"
REM Normal Maps
python photometricNormals.py --maps
REM Diffuse 
python photometricNormals.py --diffuseProj
CD %pathToMeshLab%
meshlabserver.exe -p %pathToScript%\diffuseProject.mlp -o %pathToScript%\diffuseAdded.ply -m vn -s %pathToScript%\blenderScript.mlx
CD %pathToScript%
REM Nehab
mesh_opt.exe diffuseAdded.ply -lambda 0.01 -fixnorm 1:4 diffuseEmbossed.obj
python photometricNormals.py --specularProj
CD %pathToMeshLab%
meshlabserver.exe -p %pathToScript%\specularProject.mlp -o %pathToScript%\forBlender.obj -m vn -s %pathToScript%\blenderScript.mlx
CD %pathToScript%
python blur.py
REM ---
REM Blender
REM After using shadermap for a displacement shadermap
pathToBlender="C:\Program Files\Blender Foundation\Blender"
CD %pathToBlender%
blender.exe -b -P %pathToScript%\blender.py
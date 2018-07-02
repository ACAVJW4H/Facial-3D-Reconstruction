# High Resolution Facial Capture using a Light Stage
Forked from [mk29142](https://github.com/mk29142), properly automated and adapted for Windows 10.

## Installation
The environment is tested a Windows 10 operating system.

* Install `Agisoft Photoscan Professional` (version 1.4 used for the experiments). `Photoscan` is used to transform the 3D model from the captured images. It is a propertiary application for which a 30-day trial licence can be used, before purchasing a professional or educational licence.
* Install `Blender` (version 2.79 used for the experiments). `Blender` is an open-source 3D computer graphics software toolset, that we use to increase the number of vertices in the model and adjust the UV settings.
* Install `Meshlab`. Its latest official released version is more than two years old. It is recommended to download the latest build from ci.appveyor.com/project/cignoni/meshlab and use this version for the `meshlabserver` API used in the reconstruction pipeline. In case the GUI is not working, the official release should be used for its interface, alongside the latest build. `Meshlab` is also an open-source application, that will be used with blender for the mesh of the model.
* Install `ShaderMap 4`, a windows-only and free for non-commercial use application that we use for generating the normal maps. For full automation of the script, a licence of it should be acquired to access the LUA API.
* Download the reconstruction code at github.com/lattas/facial-3d-reconstruction .
* `pipeline2.bat` is the main script for the reconstruction. All the paths pointing to the installations of the above applications
must be updated to match those of your system.
* Install the official Microsoft C++ compiler for python2.7.
* Set up a Python 2.7 (virtual) environment and install the requirements using `pip install -r requirements.txt`

## Operation

* Capture the photos using the light stage. There should be 16 photos taken by each of the 9 cameras.
* Place the photos in folders names `card\textit{i}\`, where `\textit{i}` is the number of the camera. Looking the cameras from behind and outisde the circle, they are numbers 1-7 from right to left on the top row and 8-9 from right to left on the bottom row. The photos in the camera should be `1-16.tif` according to the order they were taken.
* Ensure that the photos are in `.tif` format, with this exact capitalisation and spelling. It is important that the conversion from the raw `.CR2` format is done with a linear gamma $1.0$. If not processed directly by the camera, an easy way is to place the photos in the `card\textit{i}\` folders and convert them in linux terminal with `ufraw-batch --out-type tiff --gamma=1.0 card*/*.CR2`.
* Execute `pipeline.bat`, the main reconstruction pipeline, which will:
  * reconstruct a 3D model using Agisoft Photoscan
  * create the diffuse and specular normal maps
  * create a meshlab project and add the coordinates of the maps
  *create a combined specular maps picture with meshlab
* When prompted, open `Shader Map` and import the combined specular maps png picture "blenderTexture.png" as a normal map and then create a displacement map with height of 100 and contrast of 108. The displacement map should overwrite the input file, keeping the same name and location.
* Press any key on the terminal, which whill then
  * Blur the high resolution map with `python blur.py`.
  * Execute \texttt{blender.py} to detail the model with the displacement map.

# RDCfileschecker

## Overview
**RDCfileschecker** is a Blender add-on designed to help quickly determine the quality of RDC capture files from renderdoc

## Installation
1. Clone or download this repository.
2. In Blender, go to **`Edit > Preferences > Add-ons > Install…`**.
3. Select the downloaded `RDCchecker.py` file.
4. Enable the add-on in the Blender add-ons list.

## Usage
1. Open your project in Blender.
2. Go to `View3D > Add > Mesh > New Object` to access the RDC file check panel.
4. Input your own folder paths and RDC files names:
   - **RDC path**: path to all the RDC files.
   - **3D Folder**: folder to store the files with 3D objects, make sure to use the full absolute path.
   - **Recapture Folder**: Folder to store the list of objects that requires recapturing again, make sure to use the full absolute path.
   - **Files name**: Names of all the files you want to check, separated by comma "," without space and without '.rdc' extension
5. Afterwards, click Import to start
6. In the 3D folder, there will be a blend file for each model and a screenshot as preview to check if there is actually good 3D models
7. In the "Recapture" folder there will be a text file with list of models that weren't imported
   
## Disclaimer
Depends on the size and quantity of the files, the process can take some time, blender may appear to not responding.
Not properly tested yet, use with caution
## Requirements
- **Blender** version 4.2.0 or higher.

## Credits
Developed by:
- Long H B

# Satellite Image Processing and Classification Tool
Project that uses Sentinel-2 satellite to download and classify spatial imagery
<br/>

## Project Structure
├── assets  
├── classification  
│   ├── montreal    
│   └── sanFrancisco    
│       ├── allbands_kMeans_4.tiff  
│       └── Figure_1.png  
├── downloadedData  
│   └── sanFrancisco  
│       └── S2B_MSIL2A_20191022T185429_N0213_R113_T10SEG_20191022T214432.SAFE  
├── env  
│   └── environment.yml  
├── kmlFiles  
│   ├── montreal  
│   │   └── montreal.kml  
│   ├── sanFrancisco  
│   │   └── sanFrancisco.kml  
├── outputImages  
│   └── sanFrancisco  
│       ├── cropped  
│       │   ├── sanFranciscoAGRI_Cropped.tiff  
│       │   └── sanFranciscoRGB_Cropped.tiff  
│       ├── sanFranciscoALLBANDS.tiff  
│       └── sanFranciscoRGB.tiff  
├── README.md  
├── ressources  
│   ├── apiKeyTemplate.txt  
│   └── apiKey.txt  
└── src  
    ----├── apiSession.py : to handle requesting and downloaded the satellite imagery  
    ----├── classification.py : to classify the imagery  
    ----├── display.py : to display the satellite imagery and the classification results  
    ----├── geometryObject.py : to handle the geometry of the are, useful when cropping  
    ----├── kmlHandler.py : to handle the kml file which will be used to get coordinates of images  
    ----├── main.py  
    ----├── maps.py : currently not used  
    ----├── projectManager.py : handles the project structure and keeps track of the imagepaths  
    ----└── rasterData.py : handles the imagery and allows for manipulation  
<br/>

___
## Process

1. Start by marking the area using google map or any equivalent and saving it to kml
2. Create project and download data using sentinelApi key 
3. Create different images using rasterData class
4. Crop images
5. Display the tiff Images
6. Apply Classification algorithm to any of the images preferably, allband image
7. Display classification image

<br/>

___
## Required Packages  
* Python 3.7+
* Numpy
* Matplotlib
* rasterio 
* osgeo
* sklearn
* gdal
* fiona
* sentinelsat

More detailed specification ca be found in env/environment.yml

<br/>

____
## Examples

<br/>

### Uncropped Image
<img src="assets/sanfrancisco.png" alt="alt text" width="700" height="500">

### Cropped Image
<img src="assets/sanFranciscoRGB_Cropped.png" alt="alt text" width="700" height="500">

### Kmeans Classification using k=4
<img src="assets/Figure_1.png" alt="alt text" width="700" height="500">

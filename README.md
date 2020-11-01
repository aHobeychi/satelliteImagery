# Satellite Image Processing and Classification Tool
Project that uses Sentinel-2 satellite to download and classify spatial imagery
<br/>

## Project Structure
├── assets  
├── env  
│   └── environment.yml  
├── kmlFiles  
│   ├── montreal.kml  
│   ├── sanfrancisco.kml  
├── projects  
│   ├── montreal  
│       ├── classfication  
│       ├── data  
│       │   └── 2019_09_18  
│       ├── images  
│       │   └── cropped  
│       └── montreal.kml  
├── README.md  
├── ressources  
│   ├── apiKeyTemplate.txt  
│   └── apiKey.txt  
└── src  
    ├── apiSession.py  
    ├── classification.py  
    ├── display.py  
    ├── geometryObject.py  
    ├── kmlHandler.py  
    ├── main.py  
    ├── projectManager.py  
    └── rasterData.py  
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
<img src="assets/sanFranciscoRGB_Uncropped.png" alt="alt text" width="700" height="500">

### Cropped Image
<img src="assets/sanfrancisco.png" alt="alt text" width="700" height="500">

### Kmeans Classification using k=4
<img src="assets/Figure_1.png" alt="alt text" width="700" height="500">
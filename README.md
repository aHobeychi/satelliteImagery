satellite image processing and tool

Start by marking the area of interest using google earth or 
https://geojson.io/#map=2/20.0/0.0 and saving it as a kml file.
Then, the program uses the kml file to fetch sentinel-2 satellite 
imagery data. From the data it creates a folder of tiff images based 
onthe different spectral bands and crops those images on the 
are of interest.


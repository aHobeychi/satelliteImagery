import os
from sklearn.cluster import KMeans
import gdal
import numpy as np


def createKmeansClassification(project, clusters, imgType='allbands'):

    imagePath = project.getImagePath(imgType)
    driverTiff = gdal.GetDriverByName('GTiff')
    rasterData = gdal.Open(imagePath)
    nbands = rasterData.RasterCount
    data = np.empty((rasterData.RasterXSize*rasterData.RasterYSize, nbands))

    for i in range(1, nbands+1):
        band = rasterData.GetRasterBand(i).ReadAsArray()
        data[:, i-1] = band.flatten()

    km = KMeans(n_clusters=clusters)
    km.fit(data)
    km.predict(data)

    out_data = km.labels_.reshape((rasterData.RasterYSize,
                                   rasterData.RasterXSize))

    outputPath = os.path.join(
        project.CLASSIMG, '{}_kMeans_{}.tiff'.format(imgType, clusters))

    if os.path.exists(outputPath):
        return

    # save the original image with gdal
    outputData = driverTiff.Create(outputPath,
                                   rasterData.RasterXSize, rasterData.RasterYSize,
                                   1, gdal.GDT_Float32)
    outputData.SetGeoTransform(rasterData.GetGeoTransform())
    outputData.SetProjection(rasterData.GetProjection())
    outputData.GetRasterBand(1).SetNoDataValue(-9999.0)
    outputData.GetRasterBand(1).WriteArray(out_data)

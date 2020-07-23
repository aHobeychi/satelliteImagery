import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
from projectManager import projectManager

# NOT WORKING - HAS TO BE WORKED ON


def visualizeSelection(project, selection, cmap=None):
    paths = project.getImageFilesPaths()

    for path in paths:
        if selection.lower() in path.lower():
            img = rasterio.open(path)
            b, g, r = img.read()
            plt.imshow(r)
            plt.imshow(b)
            plt.imshow(g)
            plt.show()
            # show(img.read(2))

import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
from projectManager import projectManager
import osmnx as ox

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


def getStreetMap(project):
    footprint = project.getFootPrint()
    graph = ox.graph_from_polygon(footprint)
    ox.plot_graph(graph)
    plt.show()


def visualizeMap(project):
    footprint = project.getFootPrint()
    a = ox.footprints.footprints_from_polygon(footprint)

    print(a['addr:street'])
    print(a['name'])
    print(a['addr:postcode'])
    print(a['addr:city'])
    # graph = ox.graph_from_polygon(footprint)
    # nodes, edges = ox.graph_to_gdfs(graph)
    # fig, ax = plt.subplots(figsize=(12, 8))
    # nodes.plot(ax=ax, facecolor='black')
    # edges.plot(ax=ax, linewidth=1, edgecolor='#BC8F8F')
    # a.plot(ax=ax, facecolor='silver', alpha=0.7)
    # plt.tight_layout()
    # plt.show()

import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gdp

"""Gets Edges and nodes of the map
"""


def getStreetGraph(project):
    polygon = project.getFootPrint()
    graph = ox.graph_from_polygon(polygon)
    return graph


"""Get Geopanda representation of the project area
"""


def getOsmFootPrint(project):
    polygon = project.getFootPrint()
    footprint = ox.footprints_from_polygon(polygon)
    return footprint


def getBuildingData(project):
    polygon = project.getFootPrint()
    return ox.footprints_from_polygon(polygon, footprint_type='buildings')


"""Plot the are as a graph
"""


def plotArea(project):
    area = getOsmFootPrint(project)
    ax = area.plot(facecolor='black')

    graph = getStreetGraph(project)
    nodes, edges = ox.graph_to_gdfs(graph)

    edges.plot(ax=ax, linewidth=1, edgecolor='#BC8F8F')

    plt.tight_layout()
    plt.show()

import os
import numpy as np
import sys
import urllib.request
import requests
import xml.etree.ElementTree as ET
from bokeh.io import output_file, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool)

def project(x):

    response = requests.get("http://api.erg.kcl.ac.uk/AirQuality/Hourly/MonitoringIndex/GroupName=London")
    root = ET.fromstring(response.content)

    latitudes = []
    longitudes =[]
    sites =[]
    AQIs = []
    AQI_colors = []

    for child in root.findall(".//*[@SpeciesCode='NO2']/..[@Latitude]"):
        x = child.get('Latitude')
        latitudes.append(x)
        x = child.get('SiteName')
        sites.append(x)
        x = child.get('Longitude')
        longitudes.append(x)

    for child in root.findall(".//*[@SpeciesCode='NO2']"):
        x = child.get('AirQualityIndex')
        AQIs.append(x)




    map_options = GMapOptions(lat=51.528308, lng=-0.3817765, map_type="roadmap", zoom=10)
    plot = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="AQIs")


    for AQI in AQIs:
        if AQI =='0':
            AQI_color = AQI.replace('0','grey')
        if AQI =='1':
            AQI_color = AQI.replace('1','green')
        if AQI =='2':
            AQI_color = AQI.replace('2','orange')
        if AQI =='3':
            AQI_color = AQI.replace('3','red')

        AQI_colors.append(AQI_color)

    source = ColumnDataSource(
    data = dict(
    lat = latitudes,
    lon = longitudes,
    color = AQI_colors))

    circle = Circle(x = "lon", y = "lat", size=16, fill_color="color", fill_alpha=0.6, line_color=None)
    plot.add_glyph(source, circle)

    plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
    output_file("gmap_plot.html")
    show(plot)



project(sys.argv[1])

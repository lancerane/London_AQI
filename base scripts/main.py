import os
import numpy as np
import sys
import urllib.request
import requests
import xml.etree.ElementTree as ET
from bokeh.io import output_file, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool)

def project():

    response = requests.get("http://api.erg.kcl.ac.uk/AirQuality/Hourly/MonitoringIndex/GroupName=London")
    root = ET.fromstring(response.content)

    latitudes = []
    longitudes =[]
    sites =[]
    AQIs = []
    AQI_colors = []
    varis = {}
    varis['species'] = 'NO2'

        # species='NO2','PM25', 'PM10', 'O3', 'SO2'

    if varis['species'] == 'NO2':

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

        if varis['species'] == 'PM10':

            for child in root.findall(".//*[@SpeciesCode='PM10']/..[@Latitude]"):
                x = child.get('Latitude')
                latitudes.append(x)
                x = child.get('SiteName')
                sites.append(x)
                x = child.get('Longitude')
                longitudes.append(x)

            for child in root.findall(".//*[@SpeciesCode='PM10']"):
                x = child.get('AirQualityIndex')
                AQIs.append(x)

        if varis['species'] == 'PM25':

            for child in root.findall(".//*[@SpeciesCode='PM25']/..[@Latitude]"):
                x = child.get('Latitude')
                latitudes.append(x)
                x = child.get('SiteName')
                sites.append(x)
                x = child.get('Longitude')
                longitudes.append(x)

            for child in root.findall(".//*[@SpeciesCode='PM25']"):
                x = child.get('AirQualityIndex')
                AQIs.append(x)

        if varis['species'] == 'O3':

            for child in root.findall(".//*[@SpeciesCode='O3']/..[@Latitude]"):
                x = child.get('Latitude')
                latitudes.append(x)
                x = child.get('SiteName')
                sites.append(x)
                x = child.get('Longitude')
                longitudes.append(x)

            for child in root.findall(".//*[@SpeciesCode='O3']"):
                x = child.get('AirQualityIndex')
                AQIs.append(x)





    map_options = GMapOptions(lat=51.528308, lng=-0.3817765, map_type="roadmap", zoom=10)
    plot = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="AQIs")


    for AQI in AQIs:
        if AQI =='0':
            AQI_color = AQI.replace('0','grey')
        if AQI =='1':
            AQI_color = AQI.replace('1','forestgreen')
        if AQI =='2':
            AQI_color = AQI.replace('2','lawngreen')
        if AQI =='3':
            AQI_color = AQI.replace('3','gold')
        if AQI =='4':
            AQI_color = AQI.replace('4','darkorange')
        if AQI =='5':
            AQI_color = AQI.replace('5','orangered')
        if AQI =='6':
            AQI_color = AQI.replace('6','red')
        if AQI =='7':
            AQI_color = AQI.replace('7','magenta')
        if AQI =='8':
            AQI_color = AQI.replace('6','blueviolet')
        if AQI =='9':
            AQI_color = AQI.replace('9','blue')
        if AQI =='10':
            AQI_color = AQI.replace('10','black')

        AQI_colors.append(AQI_color)

    source = ColumnDataSource(
    data = dict(
    lat = latitudes,
    lon = longitudes,
    color = AQI_colors))

    circle = Circle(x = "lon", y = "lat", size=16, fill_color="color", fill_alpha=0.6, line_color=None)
    plot.add_glyph(source, circle)

    plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
    output_file('gmap_plot.html')
    show(plot)


if __name__ == '__main__':
    project()
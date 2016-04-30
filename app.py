from flask import Flask,render_template,request
import os
import requests
import xml.etree.ElementTree as ET
from bokeh.io import output_file, show, save
from bokeh.models import GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, HoverTool, WheelZoomTool, BoxSelectTool
from bokeh.embed import components

app = Flask(__name__)

app.vars = {}

@app.route('/', methods=['GET','POST'])
def main():

    if request.method == 'GET':
        return render_template('species_MC.html')

    else:
        #request was a POST
        app.vars['species'] = request.form['selected_species']

        response = requests.get("http://api.erg.kcl.ac.uk/AirQuality/Hourly/MonitoringIndex/GroupName=London")
        root = ET.fromstring(response.content)

        latitudes = []
        longitudes =[]
        sites =[]
        AQIs = []
        AQI_colors = []

        if app.vars['species'] == 'nitrogen dioxide':

            for child in root.findall(".//*[@SpeciesCode='NO2']/..[@Latitude]"):
                x = child.get('Latitude')
                latitudes.append(x)
                x = child.get('SiteName')
                sites.append(x)
                x = child.get('Longitude')
                longitudes.append(x)
                x = child.get('BulletinDate')
                app.vars['date'] = x

            for child in root.findall(".//*[@SpeciesCode='NO2']"):
                x = child.get('AirQualityIndex')
                AQIs.append(x)

        elif app.vars['species'] == 'PM10 particulate matter':
            app.vars['species'] = 'PM10'

            for child in root.findall(".//*[@SpeciesCode='PM10']/..[@Latitude]"):
                x = child.get('Latitude')
                latitudes.append(x)
                x = child.get('SiteName')
                sites.append(x)
                x = child.get('Longitude')
                longitudes.append(x)
                x = child.get('BulletinDate')
                app.vars['date'] = x

            for child in root.findall(".//*[@SpeciesCode='PM10']"):
                x = child.get('AirQualityIndex')
                AQIs.append(x)

        elif app.vars['species'] == 'PM25 particulate matter':
            app.vars['species'] = 'PM25'

            for child in root.findall(".//*[@SpeciesCode='PM25']/..[@Latitude]"):
                x = child.get('Latitude')
                latitudes.append(x)
                x = child.get('SiteName')
                sites.append(x)
                x = child.get('Longitude')
                longitudes.append(x)
                x = child.get('BulletinDate')
                app.vars['date'] = x

            for child in root.findall(".//*[@SpeciesCode='PM25']"):
                x = child.get('AirQualityIndex')
                AQIs.append(x)

        elif app.vars['species'] == 'ozone':

            for child in root.findall(".//*[@SpeciesCode='O3']/..[@Latitude]"):
                x = child.get('Latitude')
                latitudes.append(x)
                x = child.get('SiteName')
                sites.append(x)
                x = child.get('Longitude')
                longitudes.append(x)
                x = child.get('BulletinDate')
                app.vars['date'] = x

            for child in root.findall(".//*[@SpeciesCode='O3']"):
                x = child.get('AirQualityIndex')
                AQIs.append(x)

        elif app.vars['species'] == 'sulphur dioxide':

            for child in root.findall(".//*[@SpeciesCode='SO2']/..[@Latitude]"):
                x = child.get('Latitude')
                latitudes.append(x)
                x = child.get('SiteName')
                sites.append(x)
                x = child.get('Longitude')
                longitudes.append(x)
                x = child.get('BulletinDate')
                app.vars['date'] = x

            for child in root.findall(".//*[@SpeciesCode='SO2']"):
                x = child.get('AirQualityIndex')
                AQIs.append(x)

        else:
            return render_template('invalid_species.html')
#lat=51.528308

        map_options = GMapOptions(lat=51.4908308, lng=-0.1407765, map_type="roadmap", zoom=10)
        plot = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, plot_width=740, plot_height=650, title="AQIs", toolbar_location="below")

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
        color = AQI_colors,
        sites = sites,
        AQIs = AQIs))


        circle = Circle(x = "lon", y = "lat", size=14, fill_color="color", fill_alpha=0.5, line_color=None)
        plot.add_glyph(source, circle)


        plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool(), HoverTool())


        hover = plot.select(dict(type=HoverTool))

        # hover.tooltips=[
        #         ("Site", "@sites"),
        #         ("AQI", "@AQIs"),
        #         ]

        hover.tooltips="""
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <link rel=stylesheet type=text/css href='{{ url_for('static',filename='style_input_ht.css')}}'>

        <div>
            <div>
                <span style="font-size: 17px; color:black;">@sites</span>

            </div>
            <div>
                <span style="font-size: 15px; color: black;">AQI</span>
                <span style="font-size: 15px; color: black;">@AQIs</span>
            </div>
        </div>
        """


        # hover = plot.select(dict(type=HoverTool))
        # hover.tooltips = OrderedDict([
        # ("Site", "@lat")])
        script, div = components(plot)

        output_file('templates/map.html')
        # save(plot)



        return render_template('map.html', script=script, div=div, species=app.vars['species'], date=app.vars['date'])


if __name__ == "__main__":
    app.run(port=33507)


# path = /Users/priyarane/Documents/data_inc/London_AQI

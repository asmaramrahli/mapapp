from flask import Flask, render_template, request, send_from_directory

import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'
map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="Mapbox Bright")

fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(
    location=[lt, ln],
    radius=6,
    popup=str(el)+" m",
    color='grey',
    fill=True,
    fill_color=color_producer(el),
    fill_opacity=0.7
))


fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("templates/Map1.html")

app=Flask(__name__, static_url_path='')

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/map/')
def map():
    return render_template('Map1.html')



if __name__=="__main__":
    app.run(debug=True)

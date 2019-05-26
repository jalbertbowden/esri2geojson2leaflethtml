import os
import json
import webbrowser

featureServerURL = 'https://services1.arcgis.com/k3vhq11XkBNeeOfM/ArcGIS/rest/services/CityBoundary/FeatureServer/0'
datasetName = 'Richmond City Boundary'
mapAttribution = '<a href="' + featureServerURL + '">' + datasetName + ' Dataset</a>'
mapCoordinates = '[37.533333, -77.466667]'
mapName = 'richmond-city-boundary'
outputMapName = datasetName + ' leaflet html map done!'
mapGeoJSON = mapName + '.geojson'
mapGeoJSONPath = '"' + mapGeoJSON + '"'
mapHTML = mapName + '.html'
localPath = 'file:///Users/j.albertbowden/Desktop/github/esri2geojson2leaflethtml/'
mapHTMLName = localPath + mapHTML
esriCall = 'esri2geojson ' + featureServerURL + ' ' + mapGeoJSON
print('esri2geojson call!')

os.system(esriCall)
print('geojson output complete!')

with open(mapGeoJSON) as jsonFile:
	dataJSON = json.load(jsonFile)
	dataJSON = json.dumps(dataJSON)
	dataJSON = 'var cityBoundary = ' + dataJSON

# http://cdn.leafletjs.com/leaflet/v1.5.1/leaflet.zip
htmlScriptLeaflet = """<script>
""" + dataJSON + """
var makeMap = function(){
  var map = L.map('map').setView(""" + mapCoordinates + """, 12);
  mapCitation = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&#169; ' + mapCitation + ' Contributors &#124; """ + mapAttribution + """',
    maxZoom: 18,
  }).addTo(map);
  var boundaryStyle = {
    color: "#222",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.15,
    fillColor: "#000"
  };
  var myStyle = {
    "color": "#fff",
    "weight": 5,
    "opacity": 0.65
  };
  var geoJsonLayer = L.geoJson(cityBoundary, {
    color: "#222",
    weight: 3.25,
    opacity: 1,
    fillOpacity: 0.15,
    fillColor: "#000"
  }).addTo(map);

};
makeMap();
</script>\n"""

f = open(mapHTML,'w')

message = """<!DOCTYPE html>
<html lang="en-us">
  <head>
    <meta charset="utf-8" />
    <title>""" + datasetName + """ Leaflet Map</title>
    <link type="text/css" rel="stylesheet" href="leaflet/leaflet.css" />
    <link type="text/css" rel="stylesheet" href="map.css" />
  </head>
  <body>
    <h1>""" + datasetName + """</h1>
    <div id="map"></div>
  </body>
<script src="leaflet/leaflet.js"></script>\n"""
message = message + htmlScriptLeaflet + '</html>'
f.write(message)
f.close()
print(outputMapName)

webbrowser.open(mapHTMLName, new=2)  # open in new tab
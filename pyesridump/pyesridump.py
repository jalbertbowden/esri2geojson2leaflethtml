#!/usr/bin/python

import sys

sys.path.append('/home/45373/users/.home/.local/lib/python2.7/site-packages/')

from esridump.dumper import EsriDumper
import json
import os
import re
import webbrowser
import urllib

# pass these in from form
# dataset_name = 'Bike Racks - Richmond, Virginia'
# map_coordinates = '[37.533333, -77.466667]'

# line dataset demo
# dataset_name = 'City Boundary - Falls, Church, Virginia'
# map_coordinates = '[38.885833, -77.172222]'

# multiline demo
# dataset_name = 'BRT Pulse - Richmond, Virginia'
# map_coordinates = '[37.533333, -77.466667]'

# geometry feature types
# polygon
# feature_server_url = 'https://services1.arcgis.com/k3vhq11XkBNeeOfM/ArcGIS/rest/services/CityBoundary/FeatureServer/0'
# points
# feature_server_url = 'https://services1.arcgis.com/k3vhq11XkBNeeOfM/ArcGIS/rest/services/BikeRack/FeatureServer/0'
# line
# feature_server_url = 'http://services1.arcgis.com/2hmXRAz4ofcdQP6p/ArcGIS/rest/services/City_Boundary_Line/FeatureServer/0'
# multiline
# feature_server_url = 'https://services1.arcgis.com/k3vhq11XkBNeeOfM/ArcGIS/rest/services/BRT_Pulse_Route/FeatureServer/0'


import cgi, cgitb

form = cgi.FieldStorage()
feature_server_url =  form.getvalue('url')
dataset_name = form.getvalue('dataset-name')

# map_coordinates = form.getvalue('coordinates')
# map_coordinates_form = str(form.getvalue('coordinates'))
map_coordinates_form = str(form.getvalue('coordinates'))

map_coords_arr = map_coordinates_form.split(', ')
#lat = float(map_coords_arr[0])
#lon = float(map_coords_arr[1])

map_coordinates = '[' + map_coords_arr[0] + ', ' + map_coords_arr[1] + ']'


# dataset_name = 'BRT Pulse - Richmond, Virginia'
# map_coordinates = '[37.533333, -77.466667]'
# feature_server_url = 'https://services1.arcgis.com/k3vhq11XkBNeeOfM/ArcGIS/rest/services/BRT_Pulse_Route/FeatureServer/0'


#print("Content-type:text/html\r\n\r\n")
#print(feature_server_url)

dataset_name = str(dataset_name)
# feature_server_url = str(feature_server_url)


# format map output name
def get_dataset_name(dataset_name):
	dataset_name = str(dataset_name)
	return re.sub(r'[^a-z0-9]+', '-', dataset_name, flags=re.I).lower()

map_name = get_dataset_name(dataset_name)
map_geojson = map_name + '.geojson'
map_html = map_name + '.html'


path_url_base = 'https://bowdenweb.com/'
local_path = path_url_base + 'esri2geojson2leaflethtml/'
output_path_end = 'esri2geojson2leaflethtml/output/'
output_path = '../html/' + output_path_end
output_path_html = path_url_base + output_path_end + map_html
output_path_geojson = path_url_base + output_path_end + map_geojson
map_geojson_path = output_path + map_geojson
map_html_path = output_path + map_html
map_htmlName = local_path + map_html




# construct anchor elements
anchor_download_attribute = 'download="' + map_geojson + '"'
anchor_download_attributes = 'class="download"' + anchor_download_attribute
attribute_none = ''
anchor_attribution_content = dataset_name + ' Dataset'

def make_html_anchor(href, content, attribute):
	html_anchor = '<a href="' + href + '"'
	if attribute == '':
		html_anchor = html_anchor
	else:
		html_anchor = html_anchor + ' ' + attribute
	html_anchor = html_anchor + '>' + content + '</a>'
	return html_anchor

anchor_download = make_html_anchor(output_path_geojson, '.geojson', anchor_download_attributes)
anchor_attribution = make_html_anchor(str(feature_server_url), anchor_attribution_content, attribute_none)


# turn esri arcgis feature server endpoint into geojson, accepts url of feature service as string, return geojson
def py_esri_dump(feature_server_url, map_geojson_path):
	print(feature_server_url)
	dd = EsriDumper(feature_server_url)
	all_features = list(dd) # get all features in one list
	
	# create output .geojson file
	# this should probably be another function...trying to take advantage of only calling EsriDumper 1x
	# thinking about it....could split this into 3 functions, get features -> output file -> output variable in js inline html
	with open(map_geojson_path, 'w') as f:
		json.dump(all_features, f)
	
	# create geojson variable for inline html script
	data_json_dump = json.dumps(all_features)
	data_json_dump = 'var esriGeoJSON = ' + data_json_dump
	return data_json_dump

data_json = py_esri_dump(feature_server_url, map_geojson_path)




# html script output variables
html_script_leaflet_start = """<script>
""" + data_json + """
var makeMap = function(){
  var map = L.map('map').setView(""" + map_coordinates + """, 12);
  mapCitation = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&#169; ' + mapCitation + ' Contributors &#124; """ + anchor_attribution + """',
    maxZoom: 18,
  }).addTo(map);"""
 
html_script_leaflet_geotype_polygon = """
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
  var geoJsonLayer = L.geoJson(esriGeoJSON, {
    color: "#222",
    weight: 3.25,
    opacity: 1,
    fillOpacity: 0.15,
    fillColor: "#000"
  }).addTo(map);
"""

html_script_leaflet_geotype_points = """
  var geoJsonLayer = L.geoJson(esriGeoJSON).addTo(map);"""


# default values, theoretically will not work
html_script_leaflet_geotype_linestring = """
var lineCoordinates = esriGeoJSON[0].geometry.coordinates;
var lineCoordinatesArray = [];

function getValidGeoJSON(lineCoordinates){
	for(var x=0; x<lineCoordinates.length;x++){
		//console.log(lineCoordinates[x][0]+ ', ' +lineCoordinates[x][1]);
		let lat = lineCoordinates[x][1];
		let lon = lineCoordinates[x][0];
		let validCoordinates = [lat, lon];
		//console.log(validCoordinates);
		lineCoordinatesArray.push(validCoordinates);
	};
};
getValidGeoJSON(lineCoordinates);
var polyline = new L.polyline(lineCoordinatesArray, {
	color: '#666',
	weight: 10,
	opacity: 1,
	fill: '#000',
	fillOpacity: .01,
	fillRule: 'evenodd'
});
polyline.addTo(map);
// zoom the map to the polyline
map.fitBounds(polyline.getBounds());"""

# should this be polyline vs. geoJson??!?!?!?!?!
html_script_leaflet_geotype_multi_linestring = """
  var lineCoordinates = esriGeoJSON[0].geometry.coordinates;
  var lineCoordinatesArray = [];
  var polylineStyle = {
	  color: "#000",
  	  dashArray: "30 10",
      weight: 7
  };
  // get coordinates for each array
  function getMultiDimensionalArrayValidGeoJSON(lineCoordinates){
  	  for(var x=0; x<lineCoordinates.length; x++){
  	  	  validCoords = getValidGeoJSON(lineCoordinates[x]);
  	  	  lineCoordinatesArray.push(validCoords);
  	  };
  };
  // get valid geojson coordinates
  function getValidGeoJSON(lineCoordinates){
  	  for(var x=0; x<lineCoordinates.length;x++){
  	  	  let lat = lineCoordinates[x][1];
  	  	  let lon = lineCoordinates[x][0];
  	  	  let validCoordinates = [lat, lon];
  	  	  return validCoordinates;
  	  };
  };
  getMultiDimensionalArrayValidGeoJSON(lineCoordinates);
  
  var polyline = new L.polyline(lineCoordinatesArray, polylineStyle).addTo(map);
  map.fitBounds(polyline.getBounds());  // zoom the map to the polyline"""

html_script_leaflet_geotype_multi_polygon = """
  var geoJsonLayer = L.geoJson(esriGeoJSON).addTo(map);"""
html_script_leaflet_geotype_multi_point = """
  var geoJsonLayer = L.geoJson(esriGeoJSON).addTo(map);"""
html_script_leaflet_geotype_geometry_collection = """
  var geoJsonLayer = L.geoJson(esriGeoJSON).addTo(map);"""
html_script_leaflet_geotype_error = """
  var geoJsonLayer = L.geoJson(esriGeoJSON).addTo(map);"""


# call leaflet map function, close off function call
html_script_leaflet_map_call = """
};
makeMap();
</script>\n"""



# create first part of html script leaflet output
# make this into a function!!
# also, second EsriDumper call....combine with first? seems like one call, output data, whatever functions for manipulating data
d = EsriDumper(feature_server_url)

# get feature geometry type of geojson data
def geojson_geometry_type(d):
	for feature in d:
		geojson_geometry_type_feature = json.dumps(feature["geometry"]["type"])
		#print('geojson geometry type feature')
		#print(geojson_geometry_type_feature)
		return json.dumps(feature["geometry"]["type"])

geojson_geometry_type_feature = geojson_geometry_type(d)


""" If a string has single or double quotes around it, remove them. Make sure the pair of quotes match. If a matching pair of quotes is not found, return the string unchanged. """
def dequote(s):
    if (s[0] == s[-1]) and s.startswith(("'", '"')):
        return s[1:-1]
    return s

geojson_geometry_type_feature = dequote(geojson_geometry_type_feature)


# get geojson geometry feature type
# docs: https://tools.ietf.org/html/rfc7946#section-3.1
def geojson_geometry_type_if(geojson_geometry_type_feature):
	if geojson_geometry_type_feature == "Polygon":
		#print('Polygon!')
		htmlScriptLeafletGeoType = html_script_leaflet_geotype_polygon
	elif geojson_geometry_type_feature == 'Point':
		#print('Point!')
		htmlScriptLeafletGeoType = html_script_leaflet_geotype_points
	elif geojson_geometry_type_feature == 'LineString':
		#print('LineString!')
		htmlScriptLeafletGeoType = html_script_leaflet_geotype_linestring
	elif geojson_geometry_type_feature == 'MultiLineString':
		# print('MultiLineString!')
		htmlScriptLeafletGeoType = html_script_leaflet_geotype_multi_linestring
	elif geojson_geometry_type_feature == 'MultiPoint':
		#print('MultiPoint!')
		htmlScriptLeafletGeoType = html_script_leaflet_geotype_multi_point
	elif geojson_geometry_type_feature == 'MultiPolygon':
		#print('MultiPolygon!')
		htmlScriptLeafletGeoType = html_script_leaflet_geotype_multi_polygon
	elif geojson_geometry_type_feature == 'GeometryCollection':
		#print('GeometryCollection!')
		htmlScriptLeafletGeoType = html_script_leaflet_geotype_geometry_collection
	else:
		#print('Something else! Not a GeoJSON Geometry Object Type!')
		# probably should call an error message function or something
		htmlScriptLeafletGeoType = html_script_leaflet_geotype_error
	return htmlScriptLeafletGeoType

html_geojson_script_inline = geojson_geometry_type_if(geojson_geometry_type_feature)


# combine leaflet syntax into functional map init call
html_script_leaflet_start = html_script_leaflet_start + html_geojson_script_inline + html_script_leaflet_map_call

# create html leaflet.js web map output document
def output_html_map(map_html_path, dataset_name, anchor_download, html_script_leaflet_start, output_path_html):
	f = open(map_html_path,'w')
	html_doc_output = """<!DOCTYPE html>
<html lang="en-us">
  <head>
    <meta charset="utf-8" />
    <title>""" + dataset_name + """ Leaflet Map</title>
    <link type="text/css" rel="stylesheet" href="https://bowdenweb.com/esri2geojson2leaflethtml/leaflet/leaflet.css" />
    <link type="text/css" rel="stylesheet" href="https://bowdenweb.com/esri2geojson2leaflethtml/map.css" />
  </head>
  <body>
    <h1>""" + dataset_name + """ """ + anchor_download + """</h1>
    <div id="map"></div>
  </body>
<script src="https://bowdenweb.com/esri2geojson2leaflethtml/leaflet/leaflet.js"></script>\n"""
	html_doc_output = html_doc_output + html_script_leaflet_start + '</html>'
	f.write(html_doc_output)
	f.close()
	print("Location:" + output_path_html)
	print # to end the CGI response headers.

# output leaflet map in html document, offering newly freed data as .geojson download
output_html_map(map_html_path, dataset_name, anchor_download, html_script_leaflet_start, output_path_html)
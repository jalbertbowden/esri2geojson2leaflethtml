# esri2geojson2leaflethtml
Python script that pulls GeoJSON data out of ESRI Arcgis servers and outputs Leaflet.js web map in HTML.

Note: this is a work in progress/proof of concept. This can and should be optimized in more ways than one.  

As is, this script is only going to work for GeoJSON with geometry of type polygon.  

## Up and Running  
[Install pyesridump](https://github.com/openaddresses/pyesridump)  
Open up `esri2geojson2leaflethtml.py` and edit the following variables for your desired output:  
`featureServerURL, datasetName, mapCoordinates, mapName`  
The example below provides the information used in the example to pull Richmond, VA's City Boundary dataset of ESRI Arcgis' servers and generates a Leaflet.js powered HTML web map showing the dataset.  
<pre><code>
featureServerURL = 'https://services1.arcgis.com/k3vhq11XkBNeeOfM/ArcGIS/rest/services/CityBoundary/FeatureServer/0'
datasetName = 'Richmond City Boundary'
mapCoordinates = '[37.533333, -77.466667]'
mapName = 'richmond-city-boundary'`
</code></pre>  

TO DO:  
Cover all GeoJSON geometry types.  
Implement setup functionality from HTML form.  
Deploy on www.  
All of the code is sloppy copy/pasta get it working...not even close to being ready for primetime.  
Open map in browser upon completion.

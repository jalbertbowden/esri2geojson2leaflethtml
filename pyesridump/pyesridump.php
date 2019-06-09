<?php
/**
* pyesridump.php of pyesridump in the browser
*
*
**/
  // form handler

  if($_POST && isset($_POST['url'], $_POST['dataset-name'], $_POST['coordinates'])) {
    $url = $_POST['url'];
    $datasetName = $_POST['dataset-name'];
    $coordinates = $_POST['coordinates'];
    $valuesOutput = '<div id="form-output"><h1>Form Output</h1>';
    $valuesOutput .= '<ul><li>' .$url. '</li>';
    $valuesOutput .= '<li>' .$coordinates. '</li>';
    $valuesOutput .= '<li>' .$datasetName. '</li></ul></div>';
    // echo $valuesOutput;

    if(!$url) {
      $errorMsg = "Please enter a URL.";
    } elseif(!$datasetName) {
      $errorMsg = "Please enter the name of the dataset.";
    } elseif(!$message) {
      $errorMsg = "Please enter coordinates necessary for web map rendering.";
    }
    // echo $errorMsg;
  };

?>
<!DOCTYPE html>
<html lang="en-US">
  <head>
    <meta charset="utf-8" />
    <title>pyesridump in the browsah</title>
    <link rel="stylesheet" type="text/css" href="pyesridump.css" />
  </head>
  <body>
    <h1><code>pyesridump</code> in the browsah</h1>
    <!-- <form method="post" action=""> -->
    <form method="post" action="/cgi-bin/pyesridump-dev.py">
      <fieldset>
        <legend>ESRI ArcGIS Server to GeoJSON Leaflet.js Web Map</legend>
        <label for="url">
          <span class="block">Server URL (ex: https://services1.arcgis.com/k3vhq11XkBNeeOfM/ArcGIS/rest/services/CityBoundary/FeatureServer/0)</span>
          <input type="url" id="url" name="url" required="required" /></label>
        <label for="dataset-name">
          <span class="block">Dataset Name (ex: Richmond City Boundary)</span>
          <input type="text" id="dataset-name" name="dataset-name" required="required" /></label>
        <label for="coordinates">
          <span class="block">Coordinates (ex: 37.533333, -77.466667)</span>
          <input type="text" id="coordinates" name="coordinates" required="required" /></label>
      </fieldset>
      <input type="submit" id="submit" value="Submit" />
    </form>
    <p><strong>Note</strong>: currently only suports feature geometries of type <code>polygon</code>, <code>points</code>, <code>line</code>, and <code>multiline</code>.</p>
    <h2>What?</h2>
    <p>An implementation of <a href="https://github.com/openaddresses/pyesridump"><code>pyesridump</code></a> in the browser, outputting to an HTML Leaflet.js web map.</p>
    <h2>Examples</h2>
    <h3>Polygon</h3>
    <ul class="xoxo">
      <li>https://services1.arcgis.com/k3vhq11XkBNeeOfM/ArcGIS/rest/services/CityBoundary/FeatureServer/0</li>
      <li>City Boundary - Richmond, Virginia</li>
      <li>37.533333, -77.466667</li>
    </ul>
    <h3>Points</h3>
    <ul class="xoxo">
      <li>https://services1.arcgis.com/k3vhq11XkBNeeOfM/ArcGIS/rest/services/BikeRack/FeatureServer/0</li>
      <li>Bike Racks - Richmond, Virginia</li>
      <li>37.533333, -77.466667</li>
    </ul>
    <h3>Line</h3>
    <ul class="xoxo">
      <li>http://services1.arcgis.com/2hmXRAz4ofcdQP6p/ArcGIS/rest/services/City_Boundary_Line/FeatureServer/0</li>
      <li>City Boundary Line - Falls Church, Virginia</li>
      <li>38.885833, -77.172222</li>
    </ul>
    <ul class="xoxo">
      <li>https://services1.arcgis.com/k3vhq11XkBNeeOfM/ArcGIS/rest/services/AlleyProject/FeatureServer/0</li>
      <li>Richmond Alley ID 0 - Richmond, Virginia</li>
      <li>37.533333, -77.466667</li>
    </ul>
    <h3>MultiLine</h3>
    <ul class="xoxo">
      <li>https://services1.arcgis.com/k3vhq11XkBNeeOfM/ArcGIS/rest/services/BRT_Pulse_Route/FeatureServer/0</li>
      <li>BRT Pulse Route - Richmond, Virginia</li>
      <li>37.533333, -77.466667</li>
    </ul>
    <h2>ESRI ArcGIS Servers</h2>
    <ul class="xoxo">
      <li><a href="http://services1.arcgis.com/2hmXRAz4ofcdQP6p/ArcGIS/rest/services">City of Falls Church, Virginia</a></li>
      <li><a href="https://services1.arcgis.com/k3vhq11XkBNeeOfM/ArcGIS/rest/services">City of Richmond, Virginia</a></li>
    </ul>



<!-- <script src="pyesridump.js"></script> -->
  </body>
</html>
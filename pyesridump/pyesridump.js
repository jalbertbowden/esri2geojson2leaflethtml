// pyesridump.js - currently for dev only
var inputURL = document.getElementById('url');
var inputCoordinates = document.getElementById('coordinates');
var inputDatasetName = document.getElementById('dataset-name');
var inputSubmit = document.getElementById('submit');

function getDatasetOutputName(str){
	var datasetOutputName = str.toLowerCase();
	datasetOutputName = datasetOutputName.replace(/ /g,"-");
	// console.log('dataset output file name: ' +datasetOutputName);
};

inputSubmit.addEventListener('click', function (event){
  // event.preventDefault();
  // console.log('submit button submission prevented!');
  inputURL = inputURL.value;
  inputCoordinates = inputCoordinates.value;
  // console.log('input coordinates: ' +inputCoordinates);
  inputDatasetName = inputDatasetName.value;
  getDatasetOutputName(inputDatasetName);
  // console.log('url: ' +inputURL+ ', coordinates: ' +inputCoordinates+ ', dataset name: ' +inputDatasetName);
});

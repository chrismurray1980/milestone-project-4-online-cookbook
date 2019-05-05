/* global dc, d3, crossfilter, $*/
var cuisine_chart = dc.pieChart('#recipe-cuisine-chart');
var country_of_origin_chart = dc.pieChart('#recipe-country-of-origin-chart');
var servings_chart = dc.pieChart('#recipe-servings-chart');
var dietary_chart = dc.rowChart('#recipe-dietary-chart');
var allergen_chart = dc.rowChart('#recipe-allergen-chart');
var difficulty_chart = dc.rowChart('#recipe-difficulty-chart');
var main_ingredient_chart = dc.barChart('#recipe-main-ingredient-chart');
var total_time_chart = dc.barChart('#recipe-total-time-chart');

var data = JSON.parse($('#data').text());
var ndx = crossfilter(data);

// create pie chart of cuisine data
var cuisine_dimension = ndx.dimension(function(d) { return d.recipeCuisine; });
var cuisine_group = cuisine_dimension.group();
cuisine_chart.height(200).width(200).dimension(cuisine_dimension).group(cuisine_group);

// create pie chart of country of origin data
var country_of_origin_dimension = ndx.dimension(function(d) { return d.recipeCountryOfOrigin; });
var country_of_origin_group = country_of_origin_dimension.group();

country_of_origin_chart.width(200).height(200).dimension(country_of_origin_dimension).group(country_of_origin_group);

// create pie chart of number of servings data
var servings_dimension = ndx.dimension(function(d) { return d.recipeServings; });
var servings_group = servings_dimension.group();

servings_chart.width(200).height(200).dimension(servings_dimension).group(servings_group);

//create row chart of dietary data
var dietary_dimension = ndx.dimension(function(d) { return d.recipeDietary; }, true);
var dietary_group = dietary_dimension.group();

dietary_chart.renderLabel(true).height(200).width(200).dimension(dietary_dimension).group(dietary_group).cap(10)
    .ordering(function(d) { return -d.value; }).xAxis().ticks(3);

//create row chart of allergen data
var allergy_dimension = ndx.dimension(function(d) { return d.recipeAllergen; }, true);
var allergy_group = allergy_dimension.group();

allergen_chart.renderLabel(true).height(200).width(200).dimension(allergy_dimension).group(allergy_group).cap(10)
    .ordering(function(d) { return -d.value; }).xAxis().ticks(3);

//create row chart of difficulty data
var difficulty_dimension = ndx.dimension(function(d) { return d.recipeDifficulty; });
var difficulty_group = difficulty_dimension.group();

difficulty_chart.renderLabel(true).height(200).width(200).dimension(difficulty_dimension).group(difficulty_group).cap(10)
    .ordering(function(d) { return -d.value; }).xAxis().ticks(3);
    
//create bar chart of main ingredient data   
var main_ingredient_dimension = ndx.dimension(dc.pluck('recipeMainIngredient'));
var main_ingredient_group = main_ingredient_dimension.group();

main_ingredient_chart.width(400).height(400).margins({ top: 10, right: 50, bottom: 30, left: 50 }).dimension(main_ingredient_dimension)
    .group(main_ingredient_group).transitionDuration(500).x(d3.scale.ordinal()).xUnits(dc.units.ordinal).xAxisLabel("Main Ingredient")
    .yAxis().ticks(5);

//create bar chart of total time data   

/*var total_time_dimension = ndx.dimension(function(d) { return d.recipePreparationTime+d.recipeCookingTime; });



var total_time_group = total_time_dimension.group();

total_time_chart.width(400).height(400).margins({ top: 10, right: 50, bottom: 30, left: 50 }).dimension(total_time_dimension)
    .group(total_time_group)
    .x(d3.scale.linear().domain([50, 70]).range([50, 70])).xAxisLabel("Total time")
    .yAxis().ticks(5);*/

var time_range=[0, 200];
var time_bin_width=30;
var time_dimension = ndx.dimension(function(d) { return d.recipePreparationTime+d.recipeCookingTime; });
var time_group = time_dimension.group(function(d) {
 // Threshold
  var time_threshold = d;
  if (time_threshold <= time_range[0]) {time_threshold = time_range[0]}
  if (time_threshold >= time_range[1]) time_threshold = time_range[1] - time_bin_width;
  return time_bin_width * Math.floor(time_threshold / time_bin_width);
});


total_time_chart.width(400).height(400).margins({top: 10, right: 20, bottom: 30, left: 30})
  .centerBar(false)
  .elasticX(true)
  .elasticY(true)
  .dimension(time_dimension)
  .group(time_group)
  .x(d3.scale.linear().domain(time_range))
  .xAxisLabel("Total time (minutes)")
  .xUnits(dc.units.fp.precision(time_bin_width))
  .round(function(d) {
    return time_bin_width * Math.floor(d / time_bin_width);
  })
  .brushOn(true)
  .yAxisLabel("Number of recipes")
  .renderHorizontalGridLines(false);

/*

depthRange = [0., 5000.];
depthBinWidth = 500.;
depthDimension = filter.dimension(function(d) { return d.Depth; });
depthGrouping = depthDimension.group(function(d) {
  // Threshold
  var depthThresholded = d;
  if (depthThresholded <= depthRange[0]) {depthThresholded = depthRange[0]};
  if (depthThresholded >= depthRange[1]) depthThresholded = depthRange[1] - depthBinWidth;
  return depthBinWidth * Math.floor(depthThresholded / depthBinWidth);
});

//-----------------------------------
depthChart = dc.barChart("#chart-depth");
dataTable = dc.dataTable("#dataTable");

//-----------------------------------
depthChart
  .width(380)
  .height(200)
  .margins({
    top: 10,
    right: 20,
    bottom: 30,
    left: 30
  })
  .centerBar(false)
  .elasticY(true)
  .dimension(depthDimension)
  .group(depthGrouping)
  .x(d3.scale.linear().domain(depthRange))
  .xUnits(dc.units.fp.precision(depthBinWidth))
  .round(function(d) {
    return depthBinWidth * Math.floor(d / depthBinWidth)
  })
  .renderHorizontalGridLines(true);

xAxis_depthChart = depthChart.xAxis();
xAxis_depthChart.tickFormat(d3.format("d"));
yAxis_depthChart = depthChart.yAxis();
yAxis_depthChart.ticks(6).tickFormat(d3.format("d")).tickSubdivide(0); // tickSubdivide(0) should remove sub ticks but not

//-----------------------------------
dataTable
  .dimension(depthDimension)
  .group(function(d) {
    return d.Id + "   " + d.Depth; // Data table does not use crossfilter group but rather a closure as a grouping function
  })
  .size(30);

//-----------------------------------
dc.renderAll();
*/

//render all charts on page
dc.renderAll();

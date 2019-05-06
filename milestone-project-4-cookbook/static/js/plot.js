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
cuisine_chart.height(300)
  .width(300)
  .dimension(cuisine_dimension)
  .group(cuisine_group)
  .title(function (d) { return 'Number of '+d.key+' recipes: ' + d.value; });

// create pie chart of country of origin data
var country_of_origin_dimension = ndx.dimension(function(d) { return d.recipeCountryOfOrigin; });
var country_of_origin_group = country_of_origin_dimension.group();
country_of_origin_chart
  .height(300)
  .width(300)
  .dimension(country_of_origin_dimension).group(country_of_origin_group)
  .title(function (d) { return 'Number of recipes from '+d.key+': ' + d.value; });

// create pie chart of number of servings data
var servings_dimension = ndx.dimension(function(d) { return d.recipeServings; });
var servings_group = servings_dimension.group();
servings_chart.width(300)
  .height(300)
  .dimension(servings_dimension).group(servings_group)
  .label(function (d){ return d.key+' servings';})
  .title(function (d) { return 'Number of recipes with '+d.key+' servings: ' + d.value; });

//create row chart of dietary data
var dietary_dimension = ndx.dimension(function(d) { return d.recipeDietary; }, true);
var dietary_group = dietary_dimension.group();
dietary_chart.renderLabel(true)
  .height(300)
  .width(300)
  .dimension(dietary_dimension).group(dietary_group)
  .cap(10)
  .title(function(d){return 'Number of recipes which are '+d.key+': '+d.value;})
  .ordering(function(d) { return -d.value; })
  .xAxis()
  .ticks(3);

//create row chart of allergen data
var allergy_dimension = ndx.dimension(function(d) { return d.recipeAllergen; }, true);
var allergy_group = allergy_dimension.group();
allergen_chart.renderLabel(true)
  .height(300)
  .width(300)
  .dimension(allergy_dimension)
  .group(allergy_group)
  .cap(10)
  .title(function(d){return 'Number of recipes which contain '+d.key+': '+d.value;})
  .ordering(function(d) { return -d.value; })
  .xAxis()
  .ticks(3);

//create row chart of difficulty data
var difficulty_dimension = ndx.dimension(function(d) { return d.recipeDifficulty; });
var difficulty_group = difficulty_dimension.group();
difficulty_chart
  .height(300)
  .width(300)
  .dimension(difficulty_dimension)
  .group(difficulty_group).cap(10)
  .title(function(d){return 'Number of recipes with difficulty '+d.key+': '+d.value;})
  .ordering(function(d) { return -d.value; })
  .xAxis()
  .ticks(3);
    
//create bar chart of main ingredient data   
var main_ingredient_dimension = ndx.dimension(dc.pluck('recipeMainIngredient'));
var main_ingredient_group = main_ingredient_dimension.group();
main_ingredient_chart
  .height(300)
  .width(600)
  .margins({ top: 10, right: 50, bottom: 30, left: 50 })
  .dimension(main_ingredient_dimension)
  .group(main_ingredient_group)
  .title(function(d){return 'Number of recipes with '+d.key+' as the main ingredient: '+d.value;})
  .transitionDuration(500)
  .x(d3.scale.ordinal())
  .xUnits(dc.units.ordinal)
  .xAxisLabel("Main Ingredient")
  .yAxisLabel("Number of recipes")
  .yAxis()
  .ticks(5);

//create bar chart of total time data 
var total_time_dimension = ndx.dimension(function (d) {
        var time = d.recipePreparationTime+d.recipeCookingTime;
        if (time < 30) {
            return '< 30';
        } else if (time >= 30 && time< 60) {
            return '< 60';
        } else if (time >= 60 && time< 90) {
            return '< 90';
        }  else if (time >= 90 && time< 120) {
            return '< 120';
        } else if (time >= 120 && time< 150) {
            return '< 150';
        }else {
            return '> 150';
        }
    });
var total_time_group = total_time_dimension.group();
total_time_chart
  .height(300)
  .width(600)
  .margins({ top: 10, right: 50, bottom: 30, left: 50 })
  .dimension(total_time_dimension)
  .group(total_time_group)
  .title(function(d){return 'Number of recipes with total time '+d.key+' minutes: '+d.value;})
  .transitionDuration(500)
  .x(d3.scale.ordinal())
  .xUnits(dc.units.ordinal)
  .xAxisLabel("Total time (minutes)")
  .yAxisLabel("Number of recipes")
  .yAxis()
  .ticks(5);

//render all charts on page
dc.renderAll();

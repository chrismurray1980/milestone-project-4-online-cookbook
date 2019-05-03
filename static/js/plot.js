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
function remove_empty_bins(source_group) {
    return {
        all:function () {
            return source_group.all().filter(function(d) {
                return d.value != 0;
            });
        }
    };
}

var total_time_dimension = ndx.dimension(function(d) { return d.recipePreparationTime+d.recipeCookingTime; });
var total_time_group = remove_empty_bins(total_time_dimension.group());

total_time_chart.width(400).height(400).margins({ top: 10, right: 50, bottom: 30, left: 50 }).dimension(total_time_dimension)
    .group(total_time_group)
    .x(d3.scale.linear().domain([20, 180]).range([20, 180])).xAxisLabel("Total time")
    .yAxis().ticks(5);
    
//render all charts on page
dc.renderAll();

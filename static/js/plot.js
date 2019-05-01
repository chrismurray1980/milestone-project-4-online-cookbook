/* global dc, d3, crossfilter, $*/

var country_of_origin_chart = dc.pieChart('#recipe-country-of-origin-chart');
var main_ingredient_chart = dc.barChart('#recipe-main-ingredient-chart');
var dietary_chart = dc.barChart('#recipe-dietary-chart');
var allergen_chart = dc.barChart('#recipe-allergen-chart');

var data = JSON.parse($('#data').text());
console.log(data);
var ndx = crossfilter(data);

var country_of_origin_dimension = ndx.dimension(function(d) { 
   return d.recipeCountryOfOrigin; 
});

var country_of_origin_group = country_of_origin_dimension.group().reduceCount();

country_of_origin_chart
   .width(400)
   .height(300)
   .dimension(country_of_origin_dimension)
   .group(country_of_origin_group)
   .on('renderlet', function(chart) {
      chart.selectAll('rect').on('click', function(d) {
         console.log('click!', d);
      });
   });
   
var main_ingredient_dimension = ndx.dimension(dc.pluck('recipeMainIngredient'));

var main_ingredient_group = main_ingredient_dimension.group();  

    main_ingredient_chart
        .width(400)
        .height(300)
        .margins({top: 10, right: 50, bottom: 30, left: 50})
        .dimension(main_ingredient_dimension)
        .group(main_ingredient_group)
        .transitionDuration(500)
        .x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .xAxisLabel("Main Ingredient")
        .yAxis().ticks(20);

var dietary_dimension = ndx.dimension(dc.pluck('recipeDietary'));

var dietary_group = dietary_dimension.group();  

    dietary_chart
        .width(400)
        .height(300)
        .margins({top: 10, right: 50, bottom: 30, left: 50})
        .dimension(dietary_dimension)
        .group(dietary_group)
        .transitionDuration(500)
        .x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .xAxisLabel("Dietary requirements")
        .yAxis().ticks(20);

var allergen_dimension = ndx.dimension(dc.pluck('recipeAllergen'));

var allergen_group = allergen_dimension.group();  

    allergen_chart
        .width(400)
        .height(300)
        .margins({top: 10, right: 50, bottom: 30, left: 50})
        .dimension(allergen_dimension)
        .group(allergen_group)
        .transitionDuration(500)
        .x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .xAxisLabel("Allergen requirements")
        .yAxis().ticks(20);

dc.renderAll();

/*var country_of_origin_group = country_of_origin.group(); //create data group

    recipe_country_of_origin_pie_chart
        .radius(130)
        .innerRadius(50)
        .height(400)
        .width(300)
        .dimension(country_of_origin)
        .group(country_of_origin_group)
        .renderLabel(true)
        .legend(dc.legend().x(110).y(350).itemWidth(60).gap(5).horizontal(true))
        .transitionDuration(500);
  chart.render();*/





/*$(document).ready(function() {
    var data=$('#data').text();
    var data_object = JSON.parse(data);
     console.log(data_object);
     console.log(data_object[0]['recipeName']);
     //console.log(data);
    console.log(JSON.parse('{ "name":"John", "age":30, "city":"New York"}'));
});*/
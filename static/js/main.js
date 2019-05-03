/* global $*/

var select_contents = {
    
    allergens:       ["Dairy", "Fish", "Peanuts", "Shellfish", "Soya", "Tree-Nuts",  "Wheat", "Other"],
    cookingtime:     [5, 10, 15, 20, 30, 45, 60, 90, 120, 150],
    countryOfOrigin: ["America", "Brazil", "China", "England", "France", "Germany", "India", 
                      "Ireland", "Italy", "Japan", "Mexico",  "Scotland", "Spain", "Thailand", "Other"],
    course:          ["Starter", "Main", "Dessert"],
    cuisine:         ["American", "Brazilian", "Chinese", "English", "French", "German", "Indian", "Irish", 
                      "Italian", "Japanese", "Mexican",  "Scottish", "Spanish", "Thai", "Other"],
    dietary:         ["Vegan", "Other"],
    difficulty:      ["Easy", "Intermediate", "Hard"],
    mainIngredient:  ["Beef", "Chicken", "Fish", "Pork", "Seafood", "Turkey", "Other"],
    mealtime:        ["Breakfast", "Lunch", "Dinner", "Snack"],
    preparationtime: [5, 10 , 15, 20, 30, 45, 60, 90, 120],
    servings:        [1, 2, 4, 6, 8, 10, 12]
    
};

$(document).ready(function() {
    
    add_options(select_contents);
    format_function();
    
    $("select").change(function() {
        var select_id = $(this).attr("id");
        if (select_id != "recipeDietary" && select_id != "recipeAllergen") {
            $('input[name=' + select_id + ']').val($('#' + select_id.toString()).val());
        }
    });
            
    $(".multiple-select").click(function() {
        var select_id = $(this).attr("id");
        if (select_id == 'recipeDietary') {
            $('input[name=' + select_id + ']').val($('#recipeDietary').val());
        }
        else if (select_id == 'recipeAllergen') {
            $('input[name=' + select_id + ']').val($('#recipeAllergen').val());
        }
    }); 
                
    $('.carousel').carousel({ interval: 5000 });
    
    $('#advanced-search').click(function(){
        $('#advanced-search-form').toggleClass('hidden');
        $('#search-form').toggleClass('hidden');
    });
    
    $('#text-search').click(function(){
        $('#advanced-search-form').toggleClass('hidden');
        $('#search-form').toggleClass('hidden');
    });
    
    $('#get_Data').click(function(){
        $('#recipe-data-plots').toggleClass('hidden');
    });
});

function add_options(option_object) {
    for (const entry of Object.entries(option_object)) {
        var i, key = entry[0], value = entry[1];
        for (i = 0; i < value.length; i++) {
            var name = '.' + key.toString() + '-menu';
            $(name).append("<option value="+value[i]+">" + value[i] + "</option>");
        }
    }
}

function format_function(){
    var href = document.location.href;
    var lastPathSegment = document.location.href.substr(href.lastIndexOf('/') + 1);
    if(lastPathSegment=='show_recipe'){
        var str = document.getElementById("recipeIngredientsDisplay").innerHTML;
        document.getElementById("recipeIngredientsDisplay").innerHTML= str.replace(/(?:\r\n|\r|\n|\r\r|\n\n| {2}.| {3}.| {4}.| {5}.|, )/g, '<br>');
        }
    }




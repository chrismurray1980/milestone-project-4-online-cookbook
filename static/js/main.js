/*var cuisine = ["American", "Italian", "Spanish", "Chinese", "French", "Japanese", "German","Thai", 
                        "Mexican", "English", "Scottish", "Irish", "Brazilian" ];
var mealtime = ["Breakfast", "Lunch", "Dinner", "Snack"];
var course = ["Starter", "Main", "Dessert"];
var difficulty = ["Easy", "Intermediate", "Hard"];
var main_ingredient = ["Chicken", "Beef", "Pork", "Fish", "Turkey", "Seafood"];
var allergens = ["Nuts", "Gluten"];*/

var dropdown_contents={cuisine: ["American", "Italian", "Spanish", "Chinese", "French", "Japanese", "German","Thai", 
                        "Mexican", "English", "Scottish", "Irish", "Brazilian"], mealtime:["Breakfast", "Lunch", "Dinner", "Snack"]};


$( document ).ready(function() {
    add_options(dropdown_contents);
    //console.log(Object.keys(dropdown_contents));
    //console.log(Object.values(dropdown_contents))
});

function add_options(option_object) {
    for (var option_name in option_object) {
        var name = '#' + option_name.toString() + '-menu';
        console.log(name);
        for (i = 0; i < option_object[option_name].length; i++) {
            $(name).append("<a class='dropdown-item' href='#'>" + option_object[option_name][i] + "</a>");
        }
    }
}

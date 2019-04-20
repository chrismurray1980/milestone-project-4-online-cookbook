var $;

$(document).ready(function() {
    add_options(select_contents);
    
    $("select").change(function() {
        var select_id = $(this).attr("id");
        
        if (select_id=="recipeDietary" || select_id=="recipeAllergen" ){
            $('input[name='+select_id +']').val($('#'+select_id.toString()).val().join(", "));
        }
        else{
            $('input[name='+select_id +']').val($('#'+select_id.toString()).val());
        }
    });
});


var select_contents = {
    allergens: ["Dairy", "Fish", "Peanuts", "Shellfish", "Soya", "Tree Nuts",  "Wheat", "Other"],
    cookingtime: ["5minutes", "10minutes", "15minutes", "20minutes", "30minutes", "45minutes", "1hour", "1.5hours", "2hours", "2.5hours"],
    countryOfOrigin: ["America", "Brazil", "China", "England", "France", "Germany", "India", "Ireland", "Italy", "Japan",
        "Mexico",  "Scotland", "Spain", "Thailand", "Other"],
    course: ["Starter", "Main", "Dessert"],
    cuisine: ["American", "Brazilian", "Chinese", "English", "French", "German", "Indian", "Irish", "Italian", "Japanese",
        "Mexican",  "Scottish", "Spanish", "Thai", "Other"],
    difficulty: ["Easy", "Intermediate", "Hard"],
    dietary: ["Vegan", "Other"],
    mainIngredient: ["Beef", "Chicken", "Fish", "Pork", "Seafood", "Turkey", "Other"],
    mealtime: ["Breakfast", "Lunch", "Dinner", "Snack"],
    preparationtime: ["5minutes", "10minutes", "15minutes", "20minutes", "30minutes", "45minutes", "1hour"],
    servings: ["1", "2", "4", "6", "8"]
};

function add_options(option_object) {
    for (const entry of Object.entries(option_object)) {
        var i, key = entry[0],
            value = entry[1];
        for (i = 0; i < value.length; i++) {
            var name = '.' + key.toString() + '-menu';
            $(name).append("<option value="+value[i]+">" + value[i] + "</option>");
        }
    }
}

(function (){
    var str = document.getElementById("recipeIngredientsDisplay").innerHTML;
    document.getElementById("recipeIngredientsDisplay").innerHTML= str.replace(/(?:\r\n|\r|\n|\r\r|\n\n| {2}.| {3}.| {4}.| {5}.|, )/g, '<br>');
    //var recipeInstructions = document.getElementById("recipeInstructions");
    console.log(str);
})();
       
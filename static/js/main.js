var $;

$(document).ready(function() {
    add_options(select_contents);
    var dietary_checkbox_array= [];
    var allergy_checkbox_array= [];
   
   $('input[type="checkbox"][id="recipeDietary"]').click(function() {

        if ($(this).prop("checked") == true) {
            dietary_checkbox_array.push(this.value);
        }
        else if ($(this).prop("checked") == false) {
            dietary_checkbox_array.splice(dietary_checkbox_array.indexOf(this.value), 1);
        }
         $('input[name="recipeDietary"]').val(dietary_checkbox_array.join(", "));
        console.log($('input[name="recipeDietary"]').val());
    });
    
   $('input[type="checkbox"][id="recipeAllergen"]').click(function() {

        if ($(this).prop("checked") == true) {
            allergy_checkbox_array.push(this.value);
        }
        else if ($(this).prop("checked") == false) {
            allergy_checkbox_array.splice(allergy_checkbox_array.indexOf(this.value), 1);
        }
         $('input[name="recipeAllergen"]').val(allergy_checkbox_array.join(", "));
        console.log($('input[name="recipeAllergen"]').val());
    });  
    
   // var allergy_checkbox_array = [];
    
   /*$('input[type="checkbox"]').click(function() {
        
        if ($(this).prop('checked')==true) {
            checkbox_array.push(this.value);
        }
        else if ($(this).prop('checked')==false) {
            checkbox_array.splice(checkbox_array.indexOf(this.value), 1);
        }
        
        var name ="input[name="+$(this).attr("id")+"]";
        console.log(name);
            
        $("input[name="+$(this).attr("id")+"]").val(checkbox_array.join(", "));
        console.log($("input[name="+$(this).attr("id")+"]").val());
    });*/
});


var select_contents = {
    cuisine: ["American", "Brazilian", "Chinese", "English", "French", "German", "Indian", "Irish", "Italian", "Japanese",
        "Mexican",  "Scottish", "Spanish", "Thai", "Other"],
    countryOfOrigin: ["America", "Brazil", "China", "England", "France", "Germany", "India", "Ireland", "Italy", "Japan",
        "Mexico",  "Scotland", "Spain", "Thailand", "Other"],
    mealtime: ["Breakfast", "Lunch", "Dinner", "Snack"],
    servings: ["1", "2", "4", "6", "8"],
    preparationtime: ["< 10 minutes", "< 20 minutes", "< 30 minutes", "< 45 minutes", "< 1 hour", "< 1.5 hours", "< 2 hours", "> 2 hours"],
    cookingtime: ["< 10 minutes", "< 20 minutes", "< 30 minutes", "< 45 minutes", "< 1 hour", "< 1.5 hours", "< 2 hours", "> 2 hours"],
    course: ["Starter", "Main", "Dessert"],
    difficulty: ["Easy", "Intermediate", "Hard"],
    mainIngredient: ["Beef", "Chicken", "Fish", "Pork", "Seafood", "Turkey", "Other"],
    allergens: ["Dairy", "Fish", "Peanuts", "Shellfish", "Soya", "Tree Nuts",  "Wheat", "Other"]
};

function add_options(option_object) {
    for (const entry of Object.entries(option_object)) {
        var i, key = entry[0],
            value = entry[1];
        for (i = 0; i < value.length; i++) {
            var name = '.' + key.toString() + '-menu';
            $(name).append("<option>" + value[i] + "</option>");
        }
    }
}

(function (){
    var str = document.getElementById("recipeIngredientsDisplay").innerHTML;
    document.getElementById("recipeIngredientsDisplay").innerHTML= str.replace(/(?:\r\n|\r|\n|\r\r|\n\n| {2}.| {3}.| {4}.| {5}.|, )/g, '<br>');
    //var recipeInstructions = document.getElementById("recipeInstructions");
    console.log(str);
})();
       
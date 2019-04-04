var $;

$(document).ready(function() {
    add_options(select_contents);
    add_form_options(select_contents);
    $(".dropdown-menu li").click(function(){
      $(this).parents(".dropdown").find('.btn').html($(this).text() + '<span></span>');
      $(this).parents(".dropdown").find('.btn').val($(this).data('value'));
    });
    
});

var select_contents = {
    cuisine: ["American", "Italian", "Spanish", "Chinese", "French", "Japanese", "German", "Thai",
        "Mexican", "English", "Scottish", "Irish", "Brazilian", "Indian", "Other"],
    countryOfOrigin: ["American", "Italian", "Spanish", "Chinese", "French", "Japanese", "German", "Thai",
        "Mexican", "English", "Scottish", "Irish", "Brazilian", "Indian", "Other"],
    mealtime: ["Breakfast", "Lunch", "Dinner", "Snack"],
    servings: ["1", "2", "4", "6", "8"],
    cookingtime: ["< 10 minutes", "< 20 minutes", "< 30 minutes", "< 45 minutes", "< 1 hour", "< 1.5 hours", "< 2 hours", "> 2 hours"],
    course: ["Starter", "Main", "Dessert"],
    difficulty: ["Easy", "Intermediate", "Hard"],
    mainIngredient: ["Chicken", "Beef", "Pork", "Fish", "Turkey", "Seafood", "Other"],
    allergens: ["Nuts", "Gluten", "Other"]
};

function add_options(option_object) {
    for (const entry of Object.entries(option_object)) {
        var i, key = entry[0],
            value = entry[1];
        for (i = 0; i < value.length; i++) {
            var name = '.' + key.toString() + '-menu';
            $(name).append("<li class='dropdown-item'>" + value[i] + "</li>");
        }
    }
}

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

var $;

$(document).ready(function() {
    add_options(dropdown_contents);
    
    $(".dropdown-menu li").click(function(){
      $(this).parents(".dropdown").find('.btn').html($(this).text() + '<span></span>');
      $(this).parents(".dropdown").find('.btn').val($(this).data('value'));
    });
    
});

var dropdown_contents = {
    cuisine: ["American", "Italian", "Spanish", "Chinese", "French", "Japanese", "German", "Thai",
        "Mexican", "English", "Scottish", "Irish", "Brazilian", "Indian", "Other"],
    mealtime: ["Breakfast", "Lunch", "Dinner", "Snack"],
    course: ["Starter", "Main", "Dessert"],
    difficulty: ["Easy", "Intermediate", "Hard"],
    main_ingredient: ["Chicken", "Beef", "Pork", "Fish", "Turkey", "Seafood", "Other"],
    allergens: ["Nuts", "Gluten", "Other"]
};

function add_options(option_object) {
    for (const entry of Object.entries(option_object)) {
        var i, key = entry[0],
            value = entry[1];
        for (i = 0; i < value.length; i++) {
            var name = '#' + key.toString() + '-menu';
            $(name).append("<li class='dropdown-item'>" + value[i] + "</li>");
        }
    }
}

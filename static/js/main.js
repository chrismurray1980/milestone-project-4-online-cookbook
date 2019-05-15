/* 
    global $
*/


// create contents for select dropdowns 

var select_contents = {
    
    countryOfOrigin: [ 'America' , 'Brazil' , 'China' , 'England' , 'France' , 'Germany' , 'India' , 
                       'Ireland' , 'Italy' , 'Japan' , 'Mexico' ,  'Scotland' , 'Spain' , 'Thailand' , 'Origin-other', 'Origin-unknown' ],
                      
    course:          [ 'Starter' , 'Main' , 'Dessert' ],
    
    cuisine:         [ 'American' , 'Brazilian' , 'Chinese' , 'English' , 'French' , 'German' , 'Indian' , 'Irish' , 
                       'Italian' , 'Japanese' , 'Mexican' ,  'Scottish' , 'Spanish' , 'Thai' , 'Cusine-other', 'Cuisine-unknown' ],
    
    difficulty:      [ 'Easy' , 'Intermediate' , 'Hard' ],
    
    mainIngredient:  [ 'Beef' , 'Chicken' , 'Fish' , 'Pork' , 'Seafood' , 'Turkey' , 'Ingredient-other' ],
    
    mealtime:        [ 'Breakfast' , 'Brunch' , 'Lunch' , 'Dinner' , 'Dessert' , 'Snack' ],
    
};


// create field array to add db content to edit/delete form fields

var field_array = [ 
    
                    'recipeCuisine' , 
                    'recipeCountryOfOrigin' , 
                    'recipeMealTime' , 
                    'recipeServings' , 
                    'recipeDifficulty' , 
                    'recipePreparationTime' , 
                    'recipeCookingTime', 
                    'recipeAllergen' , 
                    'recipeDietary' , 
                    'recipeMainIngredient' 
                
                ];
                                        
                                        
var dietary_array  = [] , 
    allergen_array = [] ; // create empty array variables for checkboxes


// variables for ingredients and instructions textboxes

var ingredient_count   = 0  , 
    instruction_count  = 0  , 
    ingredient_values  = '' , 
    instruction_values = '' ; 


// add options to select dropdowns function definition

function add_options( option_object ) {
    
    for ( const entry of Object.entries( option_object ) ) {
        
        var i, key = entry[0], value = entry[1];
        
        for ( i = 0; i < value.length; i++ ) {
            
            var name = '.' + key.toString() + '-menu';
            
            $(name).append('<option value='+value[i]+'>' + value[i] + '</option>');
            
        }
        
    }
    
}


// await document readiness

$( document ).ready( function() {
    
    
    // stop enter key submitting forms on press other than text-search-form
    
    $( 'form:not( #text-search-form )' ).keypress(
        
        function( event ) {
            
            if ( event.which == '13' ) {
                
                event.preventDefault();
                
            }
            
        }
        
    );
    
    
    // define carousel change interval
    
    $( '.carousel' ).carousel( { interval: 5000 } );
    
    
    // toggle show advanced search
    
    $( '#advanced-search' ).click( function(){
        
        $( '#advanced-search-form' ).toggleClass( 'hidden' );
        
        $( '#search-form' ).toggleClass( 'hidden' );
        
    });
    
    
    // toggle show search text form
    
    $( '#text-search' ).click( function(){
        
        $( '#advanced-search-form' ).toggleClass( 'hidden' );
        
        $( '#search-form' ).toggleClass( 'hidden' );
        
    });
    
    
    // toggle show data plots
    
    $( '#get_Data' ).click( function(){
        
        $( '#recipe-data-plots' ).toggleClass( 'hidden' );
        
    });
    
    
    // check if page is showing recipe ingredients
    
    if ( $( '#recipeIngredientsDisplay' ).length ){
        
        // run iffy to format ingredients text
        
        ( function (){
            
                var str = document.getElementById( 'recipeIngredientsDisplay' ).innerHTML;
                
                document.getElementById( 'recipeIngredientsDisplay' ).innerHTML = str.replace( /(?:\r\n|\r|\n|\r\r|\n\n| {2}.| {3}.| {4}.| {5}.|, )/g, '<br>' );
                
        })();
        
    }
    
    
    // add select options to form dropdowns
    
    add_options( select_contents ); 


    // append select value to submission input text box for db submission
    
    $( 'select' ).change( function() {
        
        var select_id = $( this ).attr( 'id' );
        
        if ( select_id != 'recipeDietary' && select_id != 'recipeAllergen' ) {
            
            $( 'input[name=' + select_id + ']' ).val( $( '#' + select_id.toString() ).val() );
            
        }
        
    });
    
    
    // append number value to submission input text box for db submission
    
    $( 'input[type=number]' ).change( function() {
        
        var select_id = $( this ).attr( 'id' );
        
        $( 'input[name=' + select_id + ']' ).val( $( '#' + select_id.toString() ).val() );
            
    });
    
    
    // append checkbox value to submission input text box for db submission
    
    $( '.dietary-checkbox' ).click( function() {
        
        dietary_array=[];
        
        $( 'input[name="Dietary"]:checked' ).each( function(){
            
            dietary_array.push(this.value);
            
        });
        
        $( 'input[name=recipeDietary]' ).val( dietary_array.join( ',' ) );
        
    });
    
    
    // append checkbox value to submission input text box for db submission
    
    $( '.allergen-checkbox' ).click( function() {
        
        allergen_array=[];
        
        $( 'input[name="Allergen"]:checked' ).each( function(){
            
            allergen_array.push(this.value);
            
        });
        
        $( 'input[name=recipeAllergen]' ).val( allergen_array.join( ',' ) );
        
    });
    
    
    // confirm ingredients button and append value to submission input textarea for db submission
 
    $( '.ingredient-confirm-button' ).click( function() {
        
        ingredient_values = '';
            
        $( '.ingredient-text' ).each( function() {
            
            ingredient_values = ingredient_values + $( this ).val() + '\r\n' ;
            
        });
         
        $( 'textarea[name=recipeIngredients]' ).val( ingredient_values.substring( 0 , ingredient_values.length-2 ) );
  
    });
    
    
    // confirm instructions button and append value to submission input textarea for db submission
    
    $( '.instruction-confirm-button' ).click( function() {
        
        instruction_values = '';
    
        $( '.instruction-text' ).each( function() {
                
            instruction_values = instruction_values + $( this ).val() + '\r\n' ;
                
         });
 
        $( 'textarea[name=recipeInstructions]' ).val( instruction_values.substring( 0 , instruction_values.length-2 ) );
  
    });
    
    
    // add ingredient textarea on button click
    
    $( '.add-ingredient-button' ).click( function() {
        
        ingredient_count = ingredient_count + 1;
        
        $( '.add-recipe-ingredients' ).append( 
            
             '<div>' +
            
            '<textarea class="form-control ingredient-text" rows="1" placeholder="Please enter ingredient"></textarea>' +
            
            '<button class="btn btn-danger my-2 my-sm-0 remove-ingredient-button" type="button">X</button>' +
            
            '</div>'
            
        );
        
        $( '.ingredient-confirm-button' ).removeClass( 'hidden' );
        
        ingredient_values = '';

    });
    
    
    // add instructions textarea on button click
    
    $( '.add-instruction-button' ).click( function() {
 
        instruction_count = instruction_count + 1;
        
        
        $( '.add-recipe-instructions' ).append(
            
            '<div>' +
            
            '<textarea class="form-control instruction-text" rows="1" placeholder="Please enter instruction"></textarea>' +
            
            '<button class="btn btn-danger my-2 my-sm-0 remove-instruction-button" type="button">X</button>' +
            
            '</div>'
            
        );
        
        $( '.instruction-confirm-button' ).removeClass( 'hidden' );
        
        instruction_values = '';
        
    });

    
    // remove ingredient textarea on button click
    
    $(document).on('click', ".remove-ingredient-button", function(e) {
        
        ingredient_count = ingredient_count - 1;
        
        $(this).parent().remove();
        
        if ( ingredient_count == 0 ){
            
            $( '.ingredient-confirm-button' ).addClass( 'hidden' );
            
            ingredient_values = '';
            
            $( 'textarea[name=recipeIngredients]' ).val( '' );
        
        }
        
    });
    
    
    // remove instruction textarea on button click
    
    $(document).on('click', ".remove-instruction-button", function(e) {
        
         instruction_count = instruction_count - 1;
        
        $(this).parent().remove();
        
        if ( instruction_count == 0 ){
            
            $( '.instruction-confirm-button' ).addClass( 'hidden' );
            
            instruction_values = '';
            
            $( 'textarea[name=recipeInstructions]' ).val( '' );
        
        }
        
    });


    // add values to dropdowns, checkboxes and text inputs from db on edit/delete recipe page
    
    if ( $( 'form' ).is( '#edit_delete_form' ) ){
        
        
        // add db values as checked/selected to checkboxes and dropdowns 
        
        for ( var i = 0;  i < field_array.length;  i++ ) {
            
            var checkbox_array=[];
            
            if ( field_array[ i ] == 'recipeDietary' || field_array[ i ] == 'recipeAllergen' ){
            
                checkbox_array = $( 'input[name=' + field_array[i] + ']' ).val().split( ',' );
                
                $.each( checkbox_array , function( i , value ) {
                
                    $( 'input[value="' + value + '"]' ).prop( 'checked' , true );
                
                });
                
            }
            
            else{
                
                var name = '#' + field_array[i];
                
                var select_value = $( 'input[name=' + field_array[i] + ']' ).val();
                
                $( name ).val( select_value ).attr( 'selected', 'selected' );
                
            }
            
        }
        
        
        // split ingredients data from db into array
        
        var ingredients_array = $( 'textarea[name=recipeIngredients]' ).val().split('\n'); 
        
        
        // append ingredient array values into ingredients textarea's for modification
        
        for ( i = 0 ; i < ingredients_array.length ; i++ ){
            
            $( '.add-recipe-ingredients' ).append(
                
            '<div>' +
            
            '<textarea class="form-control ingredient-text" rows="1" placeholder="Please enter ingredient">' + ingredients_array[ i ] + '</textarea>' +
            
            '<button class="btn btn-danger my-2 my-sm-0 remove-ingredient-button" type="button">X</button>'+
            
            '</div>'
            
            );
        
            $( 'input[id=ingredient-confirm-button]' ).removeClass( 'hidden' );
            
        }
        
        
        // split instructions data from db into array
        
        var instructions_array = $( 'textarea[name=recipeInstructions]' ).val().split('\n'); 
        
        
        // append instructions array values into instructions textarea's for modification
        
        for ( i = 0 ; i < instructions_array.length ; i++ ){
            
            $( '.add-recipe-instructions' ).append(
                
            '<div>' +
            
            '<textarea class="form-control instruction-text" rows="1" placeholder="Please enter instructions">' + instructions_array[ i ] + '</textarea>' +
            
            '<button class="btn btn-danger my-2 my-sm-0 remove-instruction-button" type="button">X</button>' +
            
            '</div>'
            
            );
            
            $( 'input[id=instruction-confirm-button]' ).removeClass( 'hidden' );
            
        }
        
    }
    
});

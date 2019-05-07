/* global $*/


var select_contents = {
    
    allergens:       [ 'Dairy' , 'Fish' , 'Peanuts' , 'Shellfish' , 'Soya' , 'Tree-Nuts' ,  'Wheat' , 'Other' , 'None' ],
    
    countryOfOrigin: [ 'America' , 'Brazil' , 'China' , 'England' , 'France' , 'Germany' , 'India' , 
                       'Ireland' , 'Italy' , 'Japan' , 'Mexico' ,  'Scotland' , 'Spain' , 'Thailand' , 'Other' ],
                      
    course:          [ 'Starter' , 'Main' , 'Dessert' ],
    
    cuisine:         [ 'American' , 'Brazilian' , 'Chinese' , 'English' , 'French' , 'German' , 'Indian' , 'Irish' , 
                       'Italian' , 'Japanese' , 'Mexican' ,  'Scottish' , 'Spanish' , 'Thai' , 'Other' ],
                      
    dietary:         [ 'Vegan' , 'Other' , 'None' ],
    
    difficulty:      [ 'Easy' , 'Intermediate' , 'Hard' ],
    
    mainIngredient:  [ 'Beef' , 'Chicken' , 'Fish' , 'Pork' , 'Seafood' , 'Turkey' , 'Other' ],
    
    mealtime:        [ 'Breakfast' , 'Lunch' , 'Dinner' , 'Snack' ],
    
};


var field_array = [ 'recipeCuisine' , 
                    'recipeCountryOfOrigin' , 
                    'recipeMealTime' , 
                    'recipeServings' , 
                    'recipeDifficulty' , 
                    'recipePreparationTime' , 
                    'recipeCookingTime', 
                    'recipeAllergen', 
                    'recipeDietary', 
                    'recipeMainIngredient' 
                                        ];


$( document ).ready( function() {
    
    
    $( document ).keypress(
        
        function( event ) {
            
            if ( event.which == '13' ) {
                
                event.preventDefault();
                
            }
            
    });
    
    
    add_options( select_contents );
    
    
    if ( $( 'form' ).is( '#edit_delete_form' ) ){
         
        for ( var i = 0;  i < field_array.length;  i++ ) {
            
            var name = '#' + field_array[i];
            
            var select_value = $( 'input[name=' + field_array[i] + ']' ).val();
            
            $( name ).val( select_value ).attr( 'selected', 'selected' );
            
        }
    }
    
    
    $( 'select' ).change( function() {
        
        var select_id = $( this ).attr( 'id' );
        
        if ( select_id != 'recipeDietary' && select_id != 'recipeAllergen' ) {
            
            $( 'input[name=' + select_id + ']' ).val( $( '#' + select_id.toString() ).val() );
            
        }
        
    });
    
    
    $( 'input[type=number]' ).change( function() {
        
        var select_id = $( this ).attr( 'id' );
        
        $( 'input[name=' + select_id + ']' ).val( $( '#' + select_id.toString() ).val() );
            
    });
        
            
    $( '.multiple-select' ).click( function() {
        
        var select_id = $( this ).attr( 'id' );
        
        if ( select_id == 'recipeDietary' ) {
            
            $( 'input[name=' + select_id + ']' ).val( $( '#recipeDietary' ).val() );
            
        }
        else if ( select_id == 'recipeAllergen' ) {
            
            $( 'input[name=' + select_id + ']' ).val( $( '#recipeAllergen' ).val() );
            
        }
        
    }); 
       
                
    $( '.carousel' ).carousel( { interval: 5000 } );
    
    
    $( '#advanced-search' ).click( function(){
        
        $( '#advanced-search-form' ).toggleClass( 'hidden' );
        
        $( '#search-form' ).toggleClass( 'hidden' );
        
    });
    
    
    $( '#text-search' ).click( function(){
        
        $( '#advanced-search-form' ).toggleClass( 'hidden' );
        
        $( '#search-form' ).toggleClass( 'hidden' );
        
    });
    
    
    $( '#get_Data' ).click( function(){
        
        $( '#recipe-data-plots' ).toggleClass( 'hidden' );
        
    });
    
    
    if ( $( '#recipeIngredientsDisplay' ).length ){
        
        ( function (){
            
                var str = document.getElementById( 'recipeIngredientsDisplay' ).innerHTML;
                
                document.getElementById( 'recipeIngredientsDisplay' ).innerHTML = str.replace( /(?:\r\n|\r|\n|\r\r|\n\n| {2}.| {3}.| {4}.| {5}.|, )/g, '<br>' );
                
        })();
        
    }
    
});


function add_options( option_object ) {
    
    for ( const entry of Object.entries( option_object ) ) {
        
        var i, key = entry[0], value = entry[1];
        
        for ( i = 0; i < value.length; i++ ) {
            
            var name = '.' + key.toString() + '-menu';
            
            $(name).append('<option value='+value[i]+'>' + value[i] + '</option>');
            
        }
        
    }
    
}


# Milestone Project 4 : Online Cookbook

This project is a web-based cokkbook which allows users to quickly view recipes and find recipes based on both a simple text search and a more advanced category search. 
The user can also register and log-in to the site to access to additional site features such as 'add a new recipe', 'edit a recipe you have added', 'delete a recipe you have added',
'like a recipe' and 'add a recipe to your favourites list'.

All the recipe and user information for the site is stored on a NoSQL database and allows quick access to recipes on the site in addition to quick recipe addition and modification.


## Planning of the online cookbook

The planning undertaken prior to beginning the project is described in the following document: [Project planning document](project_planning.md) 

## Add wireframe development

## Site features

For clarity, site features will be outlined in terms of how they are implemented in each of the HTML templates.

### base.html

As the name suggests, the base.html template is used as the basis for the more content specific html templates on the site: each of which will add unique content to 
the standard base.html.

The base.html template consists of a navbar which contains the site logo and the navigation links for the the pages on the site. The site logo, itself, provides a
link anchor which will return the user to the index.html page upon click. This allows the user to easily access the home page from any other page on the website. 

In addition to this, the navigation links are log-in status specific. For example, the add-recipe and favourites links will always be visible but upon click you will only be
redirected to the correct page if you are currently logged-in otherwise you will be redirected to the log-in page after which you will be redirected to the correct page.

Furthermore, if you are not currently logged in: two additional links will be shown. These are log-in and register, clicking on these will redirect the user to the correct 
webpage. If the user is currently logged in, the log-in and register link buttons are replaced with the my-recipes and log-out buttons. The my-recipes button shows the 
recipes added directly by the current user and the log-out button will terminate the user session and return the log-in and register link buttons.

Following the header element, the html document contains the sections where the other page specific content is added e.g. search_results.html would insert the 
recipes found as a result of the search here.

At the bottom of the page is where the footer is located and this contains copyright information for the website.

### index.html

This is the landing page for the site and, firstly, contains a search box to allow the user to enter text to find a list of recipes containing that specific, case insensitive text. 
Following this are three buttons. The first of which is the 'search' button which submits the search text in the search box and returns a list of recipes containing that text; 
the second is the 'advanced search' button which hides the search box and the three buttons and reveals the advanced search form; the third button is the browse all button which 
will return a list of all recipes ordered in terms of the recipes with the highest number of likes to the lowest number of likes. 

#### Advanced search form
As mentioned above, when the 'advanced search' button is clicked: the advanced search form is revealed. This includes the 'text' button which, when clicked, will hide the advanced search form
and 'text' button and return the search box and the three original buttons. The advanced form itself consists of various dropdowns and checkboxes to allow the user to specify
multiple search conditions for the recipe search. This search form is submitted by clicking the 'submit' button at the bottom of the form. 

#### Recipe carousel 

Following the search and advanced search areas of the page there is a recipe carousel which will display the top 5 recipes on the website based upon the number
of likes. Each of these recipes is in the form of a card which contain an image of the recipe itself followed by the recipe name and some information on that recipe such as
recipe author; cuisine; number of servings; preparation and cooking times; difficulty; mealtime; and number of recipe likes. Finally, each recipe has a 'view recipe' button
which will allow the user to navigate to the 'show recipe' page for that specific recipe.

The user can manually scroll through the recipes within the carousel by clicking the next and previous arrow buttons alternatively, the recipe will change on 5 second intervals.

#### Data plots

Following the recipe carousel there is a 'show recipe data' button which shows or hides the dc.js plots of the recipe data. These data plots consist of pie charts for 
recipes by cuisine; recipes by country of origin; and recipes by number of servings. Row charts display recipes by allergen; recipes by dietary requirements; and recipes by
difficulty. Finally, bar charts show recipes by main ingredient; and recipes by combined preparation and cooking times. Whenever a user modifies one of the charts a reset 
button becomes visible to reset that specific chart. Finally, a 'reset all' button will reset all the plots whether they have been modified or not.

### show_recipe.html

When a user chooses to view the recipe they are directed to the show_recipe.html template which extends the base template: adding its unique page content. In this case
the user is directed to the recipe page with information relating directly to the recipe id selected. 

At the top of this page the recipe name is displayed followed by an image of the recipe. Following this is further information relating to this specific recipe. Below this, 
recipe ingredients and recipe step-by step instructions are shown for the recipe.

If the user is not logged-in then the page is complete. However, if the user is logged-in and the user hasn't created this recipe then two buttons appear which let the user
like abd favourite the recipe. When the user likes the recipe: the like count for the recipe is incremented by one and the 'like' button is replaced by the 'unlike' button. Clicking 
the 'unlike' button will decrement the like count and return the 'like' button to the page. Similarly, for the favourites button: when clicked the recipe is added to the
users list of favourite recipes and can be viewed in their 'favourites' page. Upon click, the 'favourite' button is replaced by the 'unfavourite' button. CLicking this button
removes the recipe from the favourites list and returns the 'favourite' button.

If the user is logged-in and is the craetor of the recipe then the 'like' and 'favourite' buttons are replaced with the 'edit/delete' recipe button. This serves two purposes:
firstly, to stop users liking and favouriting their own recipes and secondly, stopping users attempting to modify recipes that they haven't created.

### add_recipe.html

Upon clicking the 'add-recipe' link, the user is redirected to the add-recipe form. This allows the user to add a new recipe to 
the website. The form consists of simple text input fields for recipe name and author fields; dropdown inputs are provided for 
the cuisine; country of origin; mealtime; difficulty; and main ingredient fields. This format is used to limit the inputs that can
be added to the database. Number of servings; preparation time; and cooking time are given as number inputs, again to control the
values that can be added to the database from the user. Dietary and allergens are given as checkbox inputs again limited to what
is acceptable to be passed to the database.

Following these inputs are the add ingredients and add instructions sections. Both these sections have add buttons which reveal
new input textboxes upon click. In addition to this a remove button is also added mext to each textbox to allow the user to delete that
specific textbox. Once the user is satisfied with the inputs they have added the user is asked to confirm these inputs via 
a confirm button. Once, the confirm button is clicked the user is informed that the ingredients or instructions are confirmed.

Finally, the user has the opportunity to add an image of the recipe. The user can upload the image from local storage which will 
ultimately be uploaded to the AWS S3 bucket for the website which contains all the user images.

To submit the recipe the user clicks the 'submit' button at the bottom of the form and they are redirected to the 'show_recipe.html'
for the recipe they have just added and this recipe is added to the users my_recipes array in the database.

### edit_delete_recipe.html

The edit recipe form is identical to the add recipe form in layout with some exceptions. Firstly, the inputs for the 
dropdowns, texboxes and checkboxes have been pre-filled with the information from the saved recipe. All of these are still 
editable. Furthermore, the inputs for the ingredients and instructions sections have also been prefilled with the information f
from the saved recipe. For the add recipe image section, the field to add a new image has not been pre-filled allowing a 
new image to be uploaded however, the current image used by the recipe is shown below the add-image input field. The final difference
between this and the add-recipe form is the 'delete recipe' button located below the submit button form the form.

On submission of the updated recipe the user is again directed to the show_recipe.html for the updated recipe. If the recipe is 
deleted by the user the page redirects to index.html.

### search_results.html

Whenever a search is performed by the user, the results of the search are displayed in the search results page. At the top of the 
page; the user is informed of the number of recipes found in the search and each recipe returned is displayed as a recipe card which 
shows an image of the recipe; recipe name; information for the that recipe; and a 'view recipe' button which will redirect the user to the show_recipe.html for that
specific recipe. In the event that no results are found for the user search: the user is informed that no recipes were found and, in addition to this, there is a 'browse all'
button which will show all the recipes based on number of likes to ensure a consistent flow for the website UX.

### my_recipes.html

When a user adds a recipe it is added to the users my_recipes array in the database. When the user clicks on the 'my-recipes'
link in the navbar they are directed to the 'my_recipes.html' page which will inform the user of the number of recipes they have added and 
will show a card of each of these recipes. This card contains an image of the recipe; recipe name; further information on the recipe; and a view recipe
button which will allow the user to view the 'show_recipe.html' for the recipe and allow access to the edit_delete_recipe button for that recipe.

If the user hasn't yet added any recipes they are informed of this and an 'add_recipe' button is provided which will allow the user to add a new recipe. 
This has been added to improve the UX of the website.

### favourites.html

When a user favourites a recipe it is added to the users favourites array in the database. When the user clicks on the 'favourites'
link in the navbar they are directed to the 'favourites.html' page which will inform the user of the number of recipes they have added to their favourites and 
will show a card of each of these recipes. This card contains an image of the recipe; recipe name; further information on the recipe; and a view recipe
button which will allow the user to view the 'show_recipe.html' for the recipe and allow access to the 'like' and 'favourite' buttons for that recipe.

If the user hasn't yet added any favourite recipes they are informed of this and an 'browse_all_recipes' button is provided which will allow the user to browse all recipes. 
This has been added to improve the UX of the website.

### login.html

When the user clicks the log-in button on the navbar they are directed to the 'login.html' page. This page contains input
fields for the user's email and password. If the user inserts an incorrect password the page is refreshed and the user is informed 
that an incorrect password has been entered. If none of the user credentials are recognised: the user is redirected to the 'register.html' page.
Once the user has logged-in they are redirected back to the home page unless the log-in was triggered by a request for a page that requires authentication wherein 
the user will be redirected to the originally requested page.

### register.html

The register user page allows new users to be added to the website's datasbase. This consists of an html form with fields for username; email; password; and confirm password.
If the password and confirm password do not match the user is informed of this and the register user page is reloaded. Upon submission, the user is added to the database and
redirected to the login page to enter the website.








## Setting up the working environment

 1. Created a git repository for the project named 'milestone-project-4-online-cookbook'
 2. Installed flask in C9
    >Used 'sudo pip3 install flask' in the terminal to install Flask and created the app.py file. I ran the app.py file with the code executed in the 'Create the Flask Application' in 
    the Mini-project of the Code Institute Data Centric Development Module to ensure functionality
 2. Created new app in heroku and logged in via the terminal using my credentials to connect the C9 project to Heroku. I added the Heroku remote to my existing repository.
 3. I then created a 'requirements.txt' file using 'pip freeze > requirements.txt' but after mulitple failed attempts due to lack of dependencies I populated this file with the packages found in 
    'Deploy application to Heroku' in the Code Institute Data Centric Development Module
 4. Added a procfile to my project to ensure that Heroku knows how to run the project as follows: using 'echo web: python app.py > Procfile'
 5. Once the application was successfully pushed to Heroku I specified the IP and Port on Heroku in the configuration settings and the app opened in Heroku to ensure functionality
 6. The 'onlineCookbook' database was then created in MongoDB Atlas with the collection named 'recipes'
 7. To create the connection between the C9 workspace I first installed dnspython and pymongo libraries using 'sudo pip3 install dnspython' and 'sudo pip3 install pymongo' and then on MongoDB Atlas chose 
    to connect to my database through a SRV string. For security, I used environment variables to connect to MongoDB Atlas. I edited the '.bashrc' file to include the MongoDB Atlas using the following commands 'cd ..' to change to my home directory then 'nano .bashrc'
    to open the file. I then typed 'export MONGO_URI= copied connection string' added my password and edited the database name and saved the file. I then closed and reopened the temrinal and typed 'echo $MONGO_URI'
    to verify the connection
 8. I then ran the code found in the ' Run Mongo Commands From a Python File ' of the Code Institute Data Centric Development Module to ensure functionality and installed Flask-PyMongo'sudo pip3 install Flask-PyMongo'
 9. The environment setup was succesfully completed when I added the index.hmtl file and successfully wrote the name of my first database entry to the page.


 

## Test Setup 
 
 1. *Installed Flask-testing extension using 'sudo pip3 install Flask-Testing' to perform unit level testing on my flask application*
 2. installed ming to provide a validation layer to the data to and from the mongo database and provide a mim: mongo in memory functionality for testing
 3. installed python blinker library to allow signals to be seen using 'sudo pip3 install blinker'
 4. created a configuration file to allow the production database and the mim databases to be selected for testing 
 5. installed coverage.py to show the code coverage of the test.py file for the app.py file.... using 'coverage html --omit=*/usr/local/lib/python3.4/dist-packages*,*test*  '  or 'coverage html --omit=*/usr/local/lib/python3.4/dist-packages*,*test*' to obtain coverage
 6. created database_config_setup function to define database to be sued dependent upon whether the main application or the test application is being run, no need for config.py any longer

## git ignore
 'git rm --cached'
 
## CSS
 1. created scss file in static folder called 'main.scss'
 2. change to the static directory usgin 'cd static' 
 3. started a watch on the scss for compiling into css using 'sass --watch main.scss' 
 
## References
Parallax https://www.w3schools.com/howto/howto_css_parallax.asp
https://www.plus2net.com/javascript_tutorial/list-adding.php
https://stackoverflow.com/questions/784539/how-do-i-replace-all-line-breaks-in-a-string-with-br-tags   ---new line replace string--
https://www.aspsnippets.com/Articles/Get-multiple-selected-checked-CheckBox-values-as-Comma-Separated-String-using-jQuery.aspx--checkboxes to string--
https://stackoverflow.com/questions/33677374/jinja2-and-bootstrap-carousel-item-active   ----set carousel item active----
https://code.tutsplus.com/tutorials/full-text-search-in-mongodb--cms-24835 -----full text search----
https://gist.github.com/cpatrick/5719077 ----text score----
https://docs.mongodb.com/manual/reference/method/db.collection.find/ ---sort---
https://docs.mongodb.com/manual/reference/operator/update/inc/index.html ---increment---
https://stackoverflow.com/questions/13241878/convert-pymongo-cursor-to-json --json object from find results---
https://www.geeksforgeeks.org/python-add-new-keys-to-a-dictionary/  --dictionary--
https://bl.ocks.org/emiguevara/4bd152a8828f6b31270702d97dc0133d ---plot.js----
http://jsfiddle.net/PBrockmann/ma3wr55k  ----histogram-----
https://stackoverflow.com/questions/5629805/disabling-enter-key-for-form --- prevent enter key default ---
https://stackoverflow.com/questions/27264504/how-to-getchecked-values-and-remove-unchecked-in-array ---checkbox array----
https://stackoverflow.com/questions/31012129/selector-not-in-jquery-not-working ---exclude id from search form----
https://www.encodedna.com/2013/07/dynamically-add-remove-textbox-control-using-jquery.htm  ---add remove text inputs---
https://stackoverflow.com/questions/988228/convert-a-string-representation-of-a-dictionary-to-a-dictionary ----string to dict----
http://flask.pocoo.org/docs/1.0/patterns/fileuploads/  ---use flask uploads---
https://github.com/MiroslavSvec/DCD_lead --user routes and templates---
https://qiita.com/hengsokvisal/items/329924dd9e3f65dd48e7 --UPLOAD AND DOWNLOAD S3 ----
https://boh717.github.io/post/flask-login-and-mongodb/  ---flask login with pymongo----
https://stackoverflow.com/questions/48934625/objectid-object-has-no-attribute-is-active-flask-login ---m,ore login manager---
https://infinidum.com/2018/08/18/making-a-simple-login-system-with-flask-login/ ---m,ore login manager---
http://www.patricksoftwareblog.com/tag/flask-login/ ---flask_login---
https://www.reddit.com/r/flask/comments/841ka3/questiondoubt_how_to_redirect_to_the_same_page/  ---last page redirect---
https://www.tutorialspoint.com/flask/flask_sessions.htm ---FLASK SESSIONS---




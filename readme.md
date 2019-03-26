# Milestone Project 4 : Online Cookbook

## Planning of the online cookbook

This online cookbook is aimed at people looking for quick access to recipes from all over the world; of varying difficulty; and with different time pressures.

### User experience

This site allows cooks of various abilities to quickly search for and view recipes. Users with a registered email address and password can add new recipes to the 
site and edit/delete the recipes they have added previously. They also have the ability to like their favourite recipes and save personal search filters.

### Vision Statement

*‘The online cookbook website will display user added recipes, preparation instructions and information associated with these recipes. Recipes can be searched on the 
site with the user filtering recipes dependent upon several categories. Logged in users can add new recipes and edit/delete the recipes that they themselves have added. 
They will also have the ability to add any recipe to their favourites list which will be displayed on their favourite’s page. Logged in users will also have the ability 
to up-vote recipes that they have prepared and the most popular recipes will be displayed to all users when accessing the site.’*

### Features list which fulfils the vision

1.	I can search for recipes based on the following search criteria:
    1.	Cuisine
    2.	Country of origin
    3.	Allergen friendly (free)
    4.	Main ingredient
    5.	Difficulty 
    6.	Recipe Author 
    7.	Most popular
    8.	Cooking time
    9.	Meal time
2.	I can save my search and give it a name to identify it
3.	The saved search will be added to the user document 
4.	I can delete my saved searches
5.	The saved search will be removed from the user document 
6.	I can save recipes to ‘my favourites’
7.	Added favourites will be added to the user document 
8.	I can remove recipes from ‘my favourites’
9.	Removed favourites will be removed from the user document 
10.	I can add a new recipe
11.	Added recipes will be added as a new recipe document 
12.	Added recipes name added to user document
13.	I can view ‘my added recipes’
14.	‘my added recipes’ stored within the user document 
15.	I can edit recipes that I have added
16.	Edited recipes will update recipe document 
17.	I can delete recipes that I have added
18.	Deleted recipes will delete recipe document in recipe collection and entry from ‘my added recipes’ from user document
19.	I can upvote recipes that I like
20.	The upvote will increment the upvote counter in the recipe document 
21.	I can remove my upvote of a recipe
22.	The removal of the upvote will increment the upvote counter in the recipe document
23.	I can view recipe data and graphical information based on the following:
    1.	Cuisine
    2.	Country of origin
    3.	Allergen friendly (free)
    4.	Main ingredient
    5.	Difficulty 
    6.	Recipe Author 
    7.	Most popular
    8.	Cooking time
    9.	Meal time
24.	Additional recipe information obtained from data contained within the recipe entry of the recipe document
25.	When I enter the site I’m shown the landing page
26.	Most popular recipes are displayed on the landing page based on the upvotes received 
27.	I can click any recipe shown to be taken to the show recipe page
28.	When I click any graphical data representation I’m shown recipes that match this criteria
29.	When I click add recipes I am taken to the add recipe form
30.	When I click edit/delete recipes I am taken to the edit/delete recipe form
31.	When I click search I’m taken to the search form
32.	I can login to the site
33.	The login criteria will be stored in the user document in the user collection
34.	I can register for the site
35.	The password associated with the user's email address will be encrypted and not visible to the database
35.	I can delete my account for the site
36.	The user document will be deleted from the user collection
37.	I can email the recipes to others to view

### User stories

*‘As a parent, I want a chicken recipe which is nut free so that my youngest child can eat the same meal as the rest of the family.’*

>The parent would access the site and click on the search button. The parent would then filter for chicken as the main ingredient and also filter for nuts in the allergen 
friendly category. The results are then displayed.

*‘As the dinner party host, I want a tasty beef dish that is quick to prepare so that I enjoy time with my guests instead of being stuck in the kitchen all evening.’*

>The host would enter the site and click the search link in the navbar. They would then filter beef as the main ingredient and select a cooking and preparation time less 
than the maximum time they wish to invest in preparing the meal.

*‘As an enthusiastic cook, I want to share my recipes with others so that I can see if others enjoy them too.’*

>The cook would enter the site and click on the add recipe link in the navbar, if they haven’t logged-in they will be asked to log-in. If they haven’t previously registered 
they will be asked to create an account. They will then redirected to the add recipe site where they can add details of their recipe, the recipe is submitted by clicking the 
add recipe button, they will then be redirected to the home page.

*‘As I have uploaded recipes to the site before, I want to change the amount of garlic in my pasta dish, so that the recipe isn’t as overpowering.’*

>The user would enter the site and click on the edit/delete recipe link in the navbar, if they haven’t logged-in they will be asked to log-in then redirected to the edit/delete 
recipe site where they can edit details of their recipe, the recipe is submitted by clicking the edit recipe button, the user will then be redirected to the home page.

*‘As I have uploaded recipes to the site before, I want to delete my recipe as I think there are better versions of this on the site already.’*

>The user would enter the site and click on the edit/delete recipe link in the navbar, if they haven’t logged-in they will be asked to log-in then redirected to the edit/delete 
recipe site where they can delete their recipe, submitted by clicking the delete recipe button. The recipe will then be completely removed from the database, the user will then 
be redirected to the home page.

*‘As a son, I want to go round to make my Italian Mother breakfast in bed on Mother’s day, I want to make a tasty Italian breakfast for her’*

>The son would access the site and click on the search button. The son would then filter for Italian as the cuisine and also filter for breakfast in the mealtime category. The results are 
then displayed.

*‘As a husband, I want to cook that vegan recipe from the site that my wife loved, so that she knows how much I appreciate her’*

>The husband would access the site and click on the favourite’s link in the navbar, if they haven’t logged-in they will be asked to log-in then redirected to the their favourite’s page where 
they can either look through their favourite recipes or filter the results to find it directly.

*‘As a cook, I have just cooked the lamb recipe from the site and want to show that I think it’s a good recipe’*

>The cook accesses the site and searches for the recipe. The cook then clicks the upvote button on the recipe, if they haven’t logged-in they will be asked to log-in then redirected back to 
the page with the upvote now in place.

### Page content and wireframes

#### Base page layout

*Header:* contains site name, links to: log-in if not already completed, personal favourites, home, edit/delete recipe, add recipe, and search.

*Footer:*  back to top and copyright

*Side bar:* shows list of recipes based on ingredients, allergens, cuisine type, dietary choice, meal time: can add multiple filters selected by user. Shows data on number of recipes based on 
ingredient, cuisine type, meal time. Shows data on most popular of recipes based on ingredient, cuisine type, meal time. 

##### Landing page

Home page on site. Contains header, footer and sidebar. Contains site title. Contains most popular recipes (information and picture) based on up-votes from users. 

![This image is not available](static/img/wireframes/landing_page.jpg)

##### Show recipe page

Shows image, ingredients, preparation and cooking time, detailed instructions for cooking. 

![This image is not available](static/img/wireframes/show_recipe_page.jpg)

##### Add recipe page

Form to add name, time, instructions, and ingredients. Contains submit recipe button. 

![This image is not available](static/img/wireframes/add_recipe_page.jpg)

##### Edit recipe page

Form to edit name, time, instructions, and ingredients, etc.  Contains edit recipe button and delete recipe button (page only visible if it is the author who created the recipe).

![This image is not available](static/img/wireframes/edit_recipe_page.jpg)

##### Search recipe page

Form containing specifics such as allergens, main ingredient, cuisine type, meal time.

![This image is not available](static/img/wireframes/search_recipe_page.jpg)

##### Search results page

Shows all recipes which match the specified criteria during the search.

![This image is not available](static/img/wireframes/search_results_page.jpg)

##### Favourite recipes page

Contains user’s favourite recipes (information and picture) based on saved recipes.

![This image is not available](static/img/wireframes/favourite_recipes_page.jpg)

##### Log-in page

Contains form for username and password and submit button.

![This image is not available](static/img/wireframes/login_page.jpg)

##### Add user page

Add new user to site.  Contains header and footer. Contains form to add new user to database.

![This image is not available](static/img/wireframes/add_user_page.jpg)

### Languages/Technologies to be used
-   Flask
-	MongoDB Atlas
-	Python 3
-	Materialize
-	Jasmine Test suite
-	JQuery
-	CSS 3
-	HTML 5
-	JS
-	Bootstrap
-	SASS
-	Jinja
-	Heroku
-	dc/d3.js
-	python bcrypt library

### Scripts and files
-	app.py: *contains all code to generate html templates; contains code to open/close connection to database and perform CRUD operations based on the template contents*
-	base.html: *contains the base html content to be used by the site pages*
	index.html: *extends base.html and is the landing page for the site, shows most popular recipes*
-	addrecipe.html: *extends base.html and allows user to add new recipe*
-	editrecipe.html: *extends base.html and allows user to edit or delete recipe*
-	favourites.html: *extends base.html and displays user favourites*
-	search.html: *extends base.html and used to search for recipes*
-	showrecipe.html: *extends base.html and shows details of recipe*
-	login.html: *extends base.html and allows user to log-in to site*
-	register.html: *extends base.html and allows user to register for site*
-	style.css: *contains styles to be used on site*
-	main.js: *contains js code to be executed by site*
-	email.js: *contains email recipe code*
-	display.js: *contains data presentation JS code*
-	Test files: *run unit level test on python and JS*
-	Procfile: *tells Heroku how to run the app*
-	requirements.txt: *list of packages to be installed to run application*

### Database schema

The document scheme used to organise the site data on Mongo DB Atlas is a hybrid approach which uses components of both normalised and de-normalised data patterns. All the documents 
required for the site are contained within a single collection and allocated a ‘type’ attribute. The ‘type’ that the documents can have are as follows:
-	User: *stores specific user data*
-	Recipe: *stores specific recipe data*

The database schema is shown below:

![This image is not available](static/img/wireframes/database_schema.jpg)

Recipe name and recipe author values are duplicated across the Recipe and User document types as these values will be regularly used whilst the remainder of the Recipe and User properties 
remain separated out.  



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
 5. installed coverage.py to show the code coverage of the test.py file for the app.py file.... using 'coverage html --omit=*/usr/local/lib/python3.4/dist-packages*,*test*  ' to obtaine coverage


 
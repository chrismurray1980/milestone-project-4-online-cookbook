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




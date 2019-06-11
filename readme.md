# Milestone Project 4 : Online Cookbook

This project is a web-based cokkbook which allows users to quickly view recipes and find recipes based on both a simple text search and a more advanced category search. 
The user can also register and log-in to the site to access to additional site features such as 'add a new recipe', 'edit a recipe you have added', 'delete a recipe you have added',
'like a recipe' and 'add a recipe to your favourites list'.

All the recipe and user information for the site is stored on a NoSQL database and allows quick access to recipes on the site in addition to quick recipe addition and modification.


## Planning of the online cookbook

[Project planning document](project_planning.md) 



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




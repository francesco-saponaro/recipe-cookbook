# Recipe Cookbook
# UX
## Project Goals
The purpose of this website is to allow users to share and search for recipes from any cultural background, for any taste, dietary requirements, budget, schedule or occasion.  
The user will be able to show support, and give input on another user's recipe through the "like" and "comment" features.  
The website is meant to widen the users's perception, both culturally and culinarily, through the open source and social nature of the website.
### Note for the assessor
Although a profile is not needed to browse for recipes or see the statistics, most of this website features like, adding a recipe,editing or deleting it, liking and commenting a recipe, deleting your own comments and go through your own profile page which includes your own and your favourite recipes, are available once registered and logged in.  
If you would like to test run the website and have fun with the features without having to create an account, you can use this account which has plenty of recipes and history on its name:  
**USERNAME: marie, PASSWORD: marie**.  
Enjoy :)

## User Stories
### First time users
* I want to browse through all recipes, to find inspiration for a meal.
* I want to browse recipes by:
    * Recipe name
    * Ingredient
    * Meal type
    * Difficulty
    * Prep time
    * Calories
    * Country
    * Dietary requirements
    * Allergens
    * High protein
* I want to do a quick search for a recipe, to find inspiration for a meal when I am short of time.
* I want to see the available stats, to see what users are most interested in.
* I want to register and log in to add, edit and delete my own recipes.
* I want to register and log in to like and unlike another user's recipe, to connect with the community and to add the recipe on my favourites bookmarked recipes section in my profile page.
* I want to register and log in to access my profile, to see if my recipes have more likes or comments or to go through my favourite recipes for inspiration.
* I want to register and log in to comment on other users recipes, to connect with the community.
### Returning users
* I want to browse through all recipes, to find inspiration for a meal.
* I want to browse recipes by:
    * Recipe name
    * Ingredient
    * Meal type
    * Difficulty
    * Prep time
    * Calories
    * Country
    * Dietary requirements
    * Allergens
    * High protein
* I want to log in to do a quick search for a recipe, to find inspiration for a meal when I am short of time.
* I want to see the available stats, to see what users are most interested in or who is most active.
* I want to log in to see which recipes are most liked or commented.
* I want to log in to add, edit and delete my own recipes.
* I want to log in to like and unlike another user's recipe, to connect with the community and to add the recipe on my favourites bookmarked recipes section in my profile page.
* I want to log in to access my profile, to see if my recipes have more likes or comments or to go through my favourite recipes for inspiration.
* I want to log in to comment on other users recipes, to connect with the community.
* I want to log in to see if any users liked my recipes.
* I want to log in to see if any users commented on my recipes and who they were.

## Design Choices
The website is fully responsive.  
Due to the large variety of users and their age group, the overall feel of the website is designed to be clear and neat to allow for a smooth and flowing experience, regardless of who the user is. With this in mind the Materialize framework was used and this design choices were made:
### Fonts
* The standard materialize fonts were kept.
### Icons
* All Icons were taken from Font awesome and were chosen based on their clearness and message conveying ability. The like icon is in the form of a heart, once clicked it will turn red to further convey the sense of community.
### Colours
* The primary colors are a combination of dark red/bordeaux and dark green, and white and light grey, making it softer on the eye.
### Styling 
* Panels, forms and containers were given a white color with a thin bordeaux border on a light grey body, making it gentle and easy to navigate. On hovering and focus, most times colour combinations are inverted and with a smooth transition.
### Images
* The recipe images were chosen based on their definition and ability to portray the dish. However, users are able to chose whichever image suit their taste. If an image is not uploaded, a placeholder image is loaded instead, informing users that no image is available.

## Wireframes
[Link to Wireframes](//francesc-droid.github.io//recipe-cookbook/wireframes/recipe-cookbook-wireframe.pdf).

## Database schema
The MongoDB database contains 13 collections:
* Allergens - populates select options.
* Calories - populates select options.
* Comments - populates recipe page, allows owner to delete its comments and to inform users who the comment belongs to.
* Countries - populates select options in the "search recipe" page, the "quick search by country" page and its "dashboard" page chart.
* Dietary requirements - populates select options and its "dashboard" page chart.
* Difficulties - populates select options and its "dashboard" page chart.
* Meal types - populates select options and its "dashboard" page chart.
* Prep times - populates select options.
* Servings - populates select options.
* Units - populates select options.
* Ingredients - this collection stores all ingredients added in the recipes collection, with no repetitions. It has no current use, however it can be useful for future updates and implementations like, for example, a "recipes by ingredient" stats chart.  
* Users - allows users to register and log in, populates many pages with session user's credentials. It also stores user's liked recipes ID's, there is no use for it at the moment but it can be useful for potential features.
* Recipes - the recipes collection connects with the above collections in order to make the website work and also populates the "quick search" pages. Additionally it has the extra fields listed below:
    * Recipe name - populates many pages and allows users to search by a recipe's name.
    * Is high protein - populates checkbox input on the "add" and "edit" recipe pages, and the "recipe" page. It allows owner to signal other users this recipes has an high amount protein and allows users to search for high protein recipes.
    * Ingredients - populates "edit" and "recipe" pages and allows users to search for a recipe by ingredient. 
    * Description - populates "edit" and "recipe" pages.
    * Recipe image URL - populates "edit" and "recipe" pages.
    * User likes - populates many pages including the "favourite recipe" section in the profile page, it allows users to like and unlike a recipe and serves to indicate a user if it has liked a recipe.
    * User likes - this integer populates many pages and allows users to see how many likes a recipe has.
    * Comments count - this integer populates many pages and allows users to see how many comments a recipe has.

## Features
### Existing features
* Register and log in 
    * Allows users to create an account and log in to take advantage of all features and be part of the community. 
* Log out
    * Allows users to log out to protect their profile.
* Add and edit a recipe
    * Allows users to add and share recipe with the community and it allows them to make changes to it in case of, for example, a change of mind, ideas for improvement or a suggestion from another user.
* Delete a recipe
    * Allows users to delete their own recipes in case of a change of heart for example. The user will be asked, in the form of a confirmation modal, if they are in fact sure they want to delete the selected recipe.   
* Like and unlike a recipe
    * Allows liking and unliking a recipe by clicking the "heart" icon in the recipe panel. The icon has a red border and a transparent background and clicking it will toggle it to the same icon but with a red background, to indicate the user it has liked the recipe. The same recipe can only be liked once and the likes count will increase or decrease by one on each like and unlike.
* Recipe panel
    * It holds basic recipe information, including recipe name, its owner, vegan and high protein icons and like and comment features. It allows users to quickly browse through recipes and to select the desired one by clicking on its title.
* Recipe page
    * It holds the complete recipe information, including the recipe image if uploaded, ingredients, allergens, dietary requirements and description. It also contains an "add comment" section and all added comments below it.
* Add and delete comments
    * Allows users to add or delete their own comments. Recipes can be commented by clicking on the comment icon either on the recipe panel or the recipe page. Upon clicking, the user will be redirected to the "add comment" section at the bottom of the recipe page. If a comment belongs to the user a "times icon" will be displayed on the side of the comment, allowing the user to delete it.
* Search for a recipe
    * Allows users to search for a recipe by recipe name, ingredient or a selection of filters. All fields are optional.
* Quick search
    * Allows users to search for a category of recipes just by clicking on its link in the dropdown or side menu.
* profile
    * This page is divided in two sections, first contains the user's recipes and the second contains the user's favourite (liked) recipes. Sections can be accessed by clicking on their own assigned panel.
* Stats charts
    * This page contains five stats charts to show the users what are the trends in the website. The user can interact with the Donut and Pie charts by clicking on the legends checkboxes to remove some information and recalculate percentages, or on the chart slices to focus information.   
    * The charts are:
        * Recipes by Meal types 3D Donut Chart
        * Recipes by Difficulty 3D Half-donut Chart
        * Recipes by country Sorted bar Chart
        * Recipes by User 3D Pie Chart
        * Recipes by Dietary requirements 3D Cylinder Chart
* Pagination
    * Pagination is available on all pages displaying more than 10 recipes. "Amount of recipes" information is available on all pages displaying recipe panels.
### Potential features
* Search recipes by User
* Make the charts dependent from each other
* Recipes by User likes Chart
* Load complete list of countries
* Admin user 
* Upload user picture, to be displayed on recipe panel and recipe page

## Technologies used
* HTML 
    * The project uses HTML5 as it is the latest and upgraded version of HTML.
* CSS
    * The project uses CSS3 as it is an easy, consistent, lightweight and fast language to style the HTML.
* JavaScript
    * The project uses Javascript to interact with the DOM.
* Python
    * The project uses Python for back end implementation.
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
    * The project uses Flask framework for the back end and for interaction with front end.
* [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/templates/)
    * The project uses Jinja2 templates for simple and quick templating, to manipulate the page with data from backend and control the logic of the template.
* [FontAwesome](https://fontawesome.com/)
    * The project uses FontAwesome to take advantage of  the extensive icons libraries.
* [Materialize](https://materializecss.com/)
    * The project uses Materialize library as it a modern responsive front-end framework.
* [Select2](https://select2.org/)
    * Select2 was used to implememt multiple options select elements.
* [JQuery](https://jquery.com/)
    * JQuery is used to assist Materialize and Select2.
* [Sweet Alert](https://sweetalert.js.org/guides/)
    * The Sweet Alert library was used for a modern and better looking alert box.
* [AmCharts](https://www.amcharts.com/)
    * AmCharts library was used to render stats charts.
* [MongoDB](https://www.mongodb.com/2)
    * MongoDB was used as the non-relational database.

## Testing
### Validation
* HTML
    * Only errors showing on HTML validator are related to jinja syntax.
* CSS
    * No errors shown on Jigsaw validator.
* Javascript
    * Only errors are shown on the dashboard HTML page script as Jinja template syntax is used in the Javascript code to pass data into the AmCharts function.
    * No errors on JSHint otherwise.
### Client stories testing
The website flow is designed so that every page available to the user is accessible through the Navbar or slider menu, which interchange depending on screen size. The "Register" and "Log in" links interchange with the "Profile" and "Log out" links depending on if the user is logged in or not.  
Defensive programming was implemented to:
* Make sure logged in or logged out users are not able to access other user`s accounts and pages by pasting their URL. On trying to do so they will be redirected to the Home page.
* Make sure users dont log in without authentication by pasting the right URL. On trying to do so they will be redirected to the Home page.
* In the case of a 404 or 500 error the user will be redirected to a page informing him of the error and with a link to go back to the Home page.
#### As a user i want:
* I want to browse through all recipes, to find inspiration for a meal.
    * As soon as the user land in the home page he will see all available recipes displayed in panels and paginated.
    * By clicking on the desired recipe he will be redirected to the recipe page.  
* I want to browse recipes by:
    * Recipe name
    * Ingredient
    * Meal type
    * Difficulty
    * Prep time
    * Calories
    * Country
    * Dietary requirements
    * Allergens
    * High protein
        * By clicking the "search" button on the top left of the page, selecting your parameters and clickin the "apply" button.
        * The "search" button is available on every page but the "profile" and "dashboard" pages.
* I want to log in to do a quick search for a recipe, to find inspiration for a meal when I am short of time.
    * The "Quick search" dropdown menu page is located in the Navbar or Side menu depending on screen sizes.
* I want to see the available stats, to see what users are most interested in or who is most active.
    * The "Dashboard" page link is located in the Navbar or Side menu depending on screen sizes.
* I want to register to add, edit and delete my own recipes.
    * The "Register" page link is available whenever logged out and located in the Navbar or Side menu depending on screen sizes.
* I want to log in to add, edit or delete a recipe.
    * The "Log in" page link is available whenever logged out and located in the Navbar or Side menu depending on screen sizes.
* I want to log in to add a recipe.
    * The "Add recipe" page button is located on the right side of the screen and available on all pages but the "Dashboard" page, whenever logged in.
    * By clicking on the button, filling the form and clicking the "Add recipe" button.
* I want to log in to edit my own recipes.
    * The "Edit recipe" page button is located on each of the user's recipe panel whenever logged in.
    * By clicking on the button, editing the form and clicking the "Edit recipe" button.
* I want to log in to delete my own recipes.
    * The "Delete recipe" button is located on each of the user's recipe panel whenever logged in.
    * By clicking on the button, and clicking the Modal's "Confirm" button.
* I want to log in to like and unlike another user's recipe, to connect with the community and to add the recipe on my favourites bookmarked recipes section in my profile page.
    * The "Like" button is located, in the form of a "Heart" icon, on each recipe panel whenever logged in.
    * By clicking on the icon the user can like and unlike the recipe, on each click it will be redirected to the current page.
* I want to log in to access my profile, to see if my recipes have more likes or comments or to go through my favourite recipes for inspiration.
    * The "Profile" page link is available whenever logged in and located in the Navbar or Side menu depending on screen sizes.
    * By clicking on the link, and clicking on either the "Your recipes" panel or the "Your favourite recipes" panel.
* I want to log in to comment on other users recipes, to connect with the community.
    * The "Comment" link is located on each recipe panel and at the top of each recipe page, whenever logged in.
    * By clicking on the icon the user is redirected to that recipe page comments section, where it'll be able leave a comment 
    * The comments section is also accessible by manually going to a recipe page and scrolling to the bottom.
* I want to log in to see a specific recipe comments
    * The "Comment" link is located on each recipe panel and at the top of each recipe page, whenever logged in.
    * By clicking on the icon the user is redirected to that recipe page comments section, where it'll be able to see all comments.
    * The comments section is also accessible by manually going to a recipe page and scrolling to the bottom.
* I want to log in to remove a comment I posted.
    * The "Delete comment" icon is located on the right side of each of the user's comment panel.
* I want to log in to see which recipes are most liked or commented.
    * The "Like" and "Comment" counts are located beside their respective icons.
* I want to log in to see if any users liked my recipes or if any users commented on my recipes and who they were.
    * The "Profile" page link is available whenever logged in and located in the Navbar or Side menu depending on screen sizes.
    * By clicking on the link, and clicking on either the "Your recipes" panel or the "Your favourite recipes" panel.
### Lighthouse
* Passed all tests
* Scores:
    * Performance - 95
    * Accessibility - 71
    * Best Practices - 100
    * SEO - 80
### Browsers
* Mozilla, Chrome, Edge and Safari all display same projected layout and have no issues at any screen sizes.
### Screen sizes
* The website is fully responsive through the Materialize grid system and media queries, starting from a screen size as small as 280px to as large as 1680px.
* All features are available and visible on every screen size. The Navbar becomes a toggled side menu on small screen sizes.
### Bugs discovered
* Upon deploying and testing the application on Iphone, I found that none of the single or multiple options Materialize select elements were responding correctly. When trying to select an element the wrong elements would be selected, this happened every single time. Therefore I decided to replace all single option select elements with the respective "browser default" version, and all multiple option select elements with the Select2 version.  
All elements now work as desired.
* I tried to sort recipes by User likes descending, however, I found that after liking a recipe, pagination would render the wrong recipes, removing some from the page and duplicating others. I tried to find out why with the assistance of a tutor but unfortunately we couldn't fix it. Therefore I decided to display recipes in no particular order which fixed the issue.
* When displaying filtered results, the "recipe name" filter info will display with a colon punctuation ":" prior to the name. I have managed to remove all other unnecessary syntax from the results with the "replace" method, however, I don't seem to be able to target this particular colon.
* When adding a comment, the comment does not immediately show in the comments section below. It will only show once leaving the page and reloading it.
* Fixed Firefox Unordered list aligning issue by adding -moz-fit-content to the width property and -moz-center to the text-align property.
* A few days prior to submitting this projects, upon trying to open the deployed version of the website, the page would throw a "Type Error - None object is not subscriptable". This would only happen if I tried to log in from my laptop, while it worked fine on my phone. I fixed this error by clearing the data on the application storage on the dev tools. Unfortunately, even with the help of a tutor, I wasn't able to find out why this happened.

## Deployment 
This project was developed using Gitpod, a [Github repository](https://github.com/francesc-droid/recipe-cookbook) was created and regular commits were pushed to the repository through Git commands.

The project was deployed to [Heroku](https://www.heroku.com/) using the following steps:
* Set environment variables and made sure they were in the gitignore file and not being tracked.
* Created requirements.txt for dependencies and Procfile to tell which file is required to run the app: pip3 freeze --local requirements.txt echo web: python app.py > Procfile. I made sure you remove the blank line from the Procfile as it might cause problems when running the app on Heroku.
* Created new Heroku app from the Heroku website by clicking "Create new app".
* Connected my app from my Github repository by clicking on the Github icon in my app's "Deploy" section, then clicked "Search" and once it found my repo I clicked "connect".
* Before I clicked "Enable automatic deployment" I needed to tell Heroku which hidden environment variables were required (the ones hidden in the env.py file), so I clicked on the "Settings" tab and then on "Reveal config vars" and added all required hidden variables.
* Went back to "Deploy" tab, clicked on "Enable automatic deployment" and then directly below it clicked on "Deploy branch"
Heroku will now receive the code from Github and start building the app using the required packages.
* After a minute or so the message "Your app was successfully deployed" appeared, I then clicked on the "View" button below that message to launch my app.
* The deployed site was now available and automatically updated whenever I pushed changes to the Github repository.
* My deployed website can be found [here](https://recipe-cookbook-fran.herokuapp.com/).

## Credits
### Code
* HTML
    * The regex pattern for the image URL validation was taken from Stack overflow.
* JavaScript and JQuery
    * The Materialize and Select2 trigger functions were taken from their respective websites. 
    * The structure code of all charts was taken from AmChart's website, all I did was inserting the data, value and categorey coming from the back end.
### Content
* Recipes 
    * All recipes and their description were taken from [BBC Good Food](https://www.bbcgoodfood.com/).
### Media 
* Images
    * All recipes images were taken from [BBC Good Food](https://www.bbcgoodfood.com/).
* Icons
    * All icons were taken from [Font Awesome](https://fontawesome.com/).
    * Favicon icon was taken from <a href="https://www.flaticon.com/authors/flat-icons" title="Flat Icons">Flat icon</a>.



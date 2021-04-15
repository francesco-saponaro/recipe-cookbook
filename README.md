# Recipe Cookbook
# UX
## Project Goals
The purpose of this website is to allow users to share and search for recipes from any cultural background, for any taste, dietary requirements, budget, timespan or occasion.  
The user will be able to show support, and give input on another user's recipe through the "like" and "comment" features.  
The website is meant to widen the users's perception, both culturally and culinarily, through the open source and social nature of the website.
### Note for the assessor
Although a profile is not needed to browse for recipes or see the statistics, most of this website features like, adding a recipe, editing or deleting it, liking and commenting a recipe, deleting your own comments and go through your own profile page which includes your own and your favourite recipes, are available once registered and logged in.  
If you would like to test run and have fun with the features meanwhile, you can use this account which has plenty of recipes and history on its name: **USERNAME: marie, PASSWORD: marie**. Enjoy :)

## User Stories
### First time users
* I want to browse through all recipes, to find inspiration for a meal
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
* I want to see the available stats, to see what users are most interested in
* I want to register and log in to add, edit and delete my own recipes
* I want to register and log in to like and unlike another user's recipe, to connect with the community and to add the recipe on my favourites bookmarked recipes section in my profile page
* I want to register and log in to comment on other users recipes, to connect with the community
### Returning users
* I want to browse through all recipes, to find inspiration for a meal
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
* I want to see the available stats, to see what users are most interested in or who is most active
* I want to log in to see which recipes are most liked or commented
* I want to log in to add, edit and delete my own recipes
* I want to log in to like and unlike another user's recipe, to connect with the community and to add the recipe on my favourites bookmarked recipes section in my profile page
* I want to log in to comment on other users recipes, to connect with the community
* I want to log in to see if any users liked my recipes
* I want to log in to see if any users commented on my recipes and who they were

## Design Choices
The webiste is fully responsive.  
Due to the large variety of users and their age group, the overall feel of the website is designed to be clear and neat to allow for a smooth and flowing experience, regardless of who the user is. With this in mind the Materialize framework was used and this design choices were made:
### Fonts
* The standard materialize fonts were kept
### Icons
* All Icons were taken from Font awesome and were chosen based on their clearness and message conveying ability. The like icon is in the form of a heart, once clicked it will turn red to further convey the sense of community
### Colours
* The primary colors are a combination of dark red/bordeaux and dark green, and white and light grey, making it softer on the eye
### Styling 
* Panels, forms and containers were given a white color with a thin bordeaux border on a light grey body, making it gentle and easy to navigate. On hovering and focus, most times colours are inverted with a smooth transition
### Images
* The recipe images were chosen based on their definition and ability to portray the dish. However, users are able to chose whichever image suit their taste. If an image is not uploaded, a placeholder image is loaded instead, informing users that no image is available

## Wireframes
[Link to Wireframes](//francesc-droid.github.io//workspace/recipe-cookbook/wireframes/recipe-cookbook-wireframe.pdf)

## Database schema
The MongoDB database contains 13 collections:
* Allergens - populates select options
* Calories - populates select options
* Comments - populates recipe page, allows owner to delete its comments and to inform users who the comment belongs to
* Countries - populates select options in the "search recipe" page, the "quick search by country" page and its "dashboard" page chart
* Dietary requirements - populates select options and its "dashboard" page chart
* Difficulties - populates select options and its "dashboard" page chart
* Meal types - populates select options and its "dashboard" page chart
* Prep times - populates select options
* Servings - populates select options
* Units - populates select options
* Ingredients - this collection stores all ingredients added in the recipes collection, with no repetitions. It has no current use, however it can be useful for future updates and implementations like, for example, a "recipes by ingredient stats chart"   
* Users - allows users to register and log in, populates many pages with session user's credentials. It also stores user's liked recipes ID's, there is no use for it at the moment but it can be useful for potential features
* Recipes - the recipes collection fields with the same name as above collections, connect with them in order to make the website work, many of its fields populate the "quick search" pages. Additionally it has the extra fields listed below:
    * Recipe name - populates many pages and allows users to search by a recipe's name
    * Is high protein - populates checkbox input on the "add" and "edit" recipe pages, and the "recipe" page. It allows owner to signal other users this recipes has an high amount protein and allows users to search for high protein recipes 
    * Ingredients - populates "edit" and "recipe" pages and allows users to search for a recipe by ingredient 
    * Description - populates "edit" and "recipe" pages
    * Recipe image URL - populates "edit" and "recipe" pages
    * User likes - populates many pages including the "favourite recipe" section in the profile page, it allows users to like and unlike a recipe and serves to indicate a user if it has liked a recipe
    * User likes - this integer populates many pages and allows users to see how many likes a recipe has
    * Comments count - this integer populates many pages and allows users to see how many comments a recipe has

## Features
### Existing features
#### Register and log in 
Allows users to create an account and log in to take advantage of all features and be part of the community 
#### Log out
Allows users to log out to protect their profile
#### Add and edit a recipe
Allows users to add and share recipe with the community and it allows them to make changes to it in case of, for example, a change of mind, ideas for improvement or a suggestion from another user
#### Delete a recipe
Allows users to delete their own recipes in case of a change of heart for example. The user will be asked, in the form of a confirmation modal, if they are in fact sure they want to delete the selected recipe   
#### Like and unlike a recipe
Allows liking and unliking a recipe by clicking the "heart" icon in the recipe panel. The icon has a red border and a transparent background and clicking it will toggle it to the same icon but with a red background, to indicate the user it has liked the recipe. The same recipe can only be liked once and the likes count will increase or decrease by one on each like and unlike
#### Recipe panel
It holds basic recipe information, including recipe name, its owner, vegan and high protein icons and like and comment features. It allows users to quickly browse through recipes and to select the desired one by clicking on its title
#### Recipe page
It holds the complete recipe information, including the recipe image if uploaded, ingredients, allergens, dietary requirements and description. It also contains an "add comment" section and all added comments below it
#### Add and delete comments
Allows users to add or delete their own comments. Recipes can be commented by clicking on the comment icon either on the recipe panel or the recipe page. Upon clicking, the user will be redirected to the "add comment" section at the bottom of the recipe page. If a comment belongs to the user a "times icon" will be displayed on the side of the comment, allowing the user to delete it
#### Search for a recipe
Allows users to search for a recipe by recipe name, ingredient or a selection of filters. All fields are optional
#### Quick search
Allows users to search for a category of recipes just by clicking on its link in the dropdown or side menu
#### profile
This page is divided in two sections, first contains the user's recipes and the second contains the user's favourite (liked) recipes. Sections can be accessed by clicking on their own assigned panel 
#### Stats charts
This page contains five stats charts to show the users what are the trends in the website. The user can interact with the Donut and Pie charts by clicking on the legends checkboxes to remove some information and recalculate percentages, or on the chart slices to focus information   
The charts are:
* Recipes by Meal types 3D Donut Chart
* Recipes by Difficulty 3D Half-donut Chart
* Recipes by country Sorted bar Chart
* Recipes by User 3D Pie Chart
* Recipes by Dietary requirements 3D Cylinder Chart
#### Pagination
Pagination is available on all pages displaying more than 10 recipes. "Amount of recipes" information is available on all pages displaying recipe panels

### Potential features
#### Search recipes by User
#### Make the charts dependent from each other
#### Recipes by User likes Chart
#### Load complete list of countries
#### Admin user 
#### Upload user picture, to be displayed on recipe panel and recipe page

## Technologies used
* HTML 
    * The project uses HTML5 as it is the latest and upgraded version of HTML
* CSS
    * The project uses CSS3 as it is an easy, consistent, lightweight and fast language to style the HTML
* JavaScript
    * The project uses Javascript to interact with the DOM
* Python
    * The project uses Python for back end implementation
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
    * The project uses Flask framework for the back end and for interaction with front end
* [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/templates/)
    * The project uses Jinja2 templates for simple and quick templating, to manipulate the page with data from backend and control the logic of the template
* [FontAwesome](https://fontawesome.com/)
    * The project uses FontAwesome to take advantage of  the extensive icons libraries
* [Materialize](https://materializecss.com/)
    * The project uses Materialize library as it a modern responsive front-end framework
* [Select2](https://select2.org/)
    * Select2 was used to implememt multiple options select elements
* [JQuery](https://jquery.com/)
    * JQuery is used to assist Materialize and Select2
* [Sweet Alert](https://sweetalert.js.org/guides/)
    * The Sweet Alert library was used for a modern and better looking alert box
* [AmCharts](https://www.amcharts.com/)
    * AmCharts library was used to render stats charts
* [MongoDB](https://www.mongodb.com/2)
    * MongoDB was used as the non-relational database

## Testing
### Validation
#### HTML
* Only errors showing on HTML validator are related to jinja syntax
#### CSS
* No errors shown on Jigsaw validator
#### Javascript
* Only errors are shown on the dashboard HTML page script as Jinja template syntax is used in the Javascript code to pass data into the AmCharts function
* No errors on JSHint otherwise
### Client stories testing

### Lighthouse
* Passed all tests
* Scores:
    * Performance - 95
    * Accessibility - 71
    * Best Practices - 100
    * SEO - 80
### Browsers
* Mozilla, Chrome, Edge and Safari all display same projected layout and have no issues at any screen sizes
### Screen sizes
* The website is fully responsive through the Materialize grid system and media queries, starting from a screen size as small as 280px to as large as 1680px.
* All features are available and visible on every screen size. The Navbar becomes a toggled side menu on small screen sizes
### Bugs discovered
* Upon deploying and testing the application on Iphone I found that none of the single or multiple options Materialize select elements were responding correctly. When trying to select an element the wrong elements would be selected, this happened every single time. Therefore I decided to replace all single option select elements with the respective "browser default" version, and all multiple option select elements with the Select2 version. All elements now work as desired
* I tried to sort recipes by User likes descending, however, I found that after liking a recipe, pagination would render the wrong recipes, removing some from the page and duplicating others. I tried to find out why with the assistance of a tutor but unfortunately we couldn't fix it. I therefore decided to display recipes in no particular order which fixed the issue
* When displaying filtered results, the "recipe name" filter info will display with a colon punctuation ":" prior to the name. I have managed to remove all other unnecessary syntax from the results with the "replace" method, however, I don't seem to be able to target this particular colon 
* When adding a comment, the comment does not immediately show in the comments section below. It will only show once leaving the page and reloading it 

## Deployment 
This project was developed using Gitpod, committed to Github and pushed to Github using the built in function.

To deploy this page to Github Pages from it's [Github repository](https://github.com/francesc-droid/ramen-locator), the following steps were taken:
1. Log into Github.
2. From the list of repositories on the screen, select "ramen-locator".
3. From the menu items near the top of the page, select "Settings".
4. Scroll down to the Github pages section.
5. Under "Source" click the drop down menu labelled "None" and select "Main" branch.
6. Click "Save" and the website is now deployed.
7. Above "Source" you will find the link to the deployed website.

### How to run this project locally
To clone this project into Gitpod you will need:
1. A Github account. Create a Github account [here](https://github.com/).
2. Use the Chrome browser.

Then follow these steps:
1. Install the Gitpod browser extension for Chrome.
2. After installation restart the browser.
3. Log into Github with your Github account.
4. Navigate to the project Github repository.
5. Click the green "Gitpod" button.
6. This will trigger a new Gitpod workspace to be created from the code in Github where you can work locally.

To work on the project code within a local IDE such as VSCode etc.
1. Follow this link to the [Project Github repository](https://github.com/francesc-droid/ramen-locator).
2. Under the repository name, click "Code" and then "Clone" or "Download ZIP".
3. In the "Clone with the HTTPs" section, copy the clone URL for the repository.
4. In your local IDE, open the terminal.
5. Change the current working directory to the location where you want the directory to be cloned.
6. Type "git clone",  and then paste the URL you copied in step 3.
7. Press "Enter" and your local clone will be created.

## Credits
### Code
#### HTML
* The regex pattern for the image URL validation was taken from Stack overflow
#### JavaScript and JQuery
* The Materialize and Select2 trigger functions were taken from their respective websites 
* The structure code of all charts was taken from AmChart's website, all I did was inserting the data, value and categorey coming from the back end
### Content
#### Recipes 
* All recipes and their description were taken from [BBC Good Food](https://www.bbcgoodfood.com/)
### Media 
#### Images
* All recipes images were taken from [BBC Good Food](https://www.bbcgoodfood.com/)
#### Icons
* All icons were taken from [Font Awesome](https://fontawesome.com/)



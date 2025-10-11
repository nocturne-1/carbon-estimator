### Carbon Estimator
Hi! This project is carbon-estimator, a web app that allows users to see the carbon footprint of each of their activities, and displays a personalized carbon footprint dashboard to show users once activity footprints have been calculated.This project was made to be shipped for the Athena Award, and more specifically, I am submitting this to the Level Up Challenge, as it is my first web project with a back-end!

## Why I Made Carbon Estimator
I made carbon estimator, because I recently attended a presentation on sustainability in everyday life at my school discussing how various activities all contribute to society's larger carbon footprint, where I understood that lowering emissions can stem from everyone making more sustainable individual choices. 

I believe more sustainable decisions can be made only once you understand the impact of your current decisions and see visually how making sustainable decisions leads to the release of fewer carbon emissions on a personal level. A great way of bringing that information to people, in my mind, was by allowing people to see the numerical amount of kg of CO2 that is released by certain actions - from energy use to transportation to accommodation. That was how carbon estimator was born: a platform to show individuals the collective and individual carbon footprint of their activities across various sectors. 

## How I Made Carbon Estimator
I used Flask and SQL-Alchemy to write data from a form into my database on the server (back-end). After configuring SQLite and setting an instance of my database (db = SQLAlchemy(app)), I created a class to structure my database (Profile) with all the columns/fields I needed in my db. When structuring my db, certain columns are allowed to be null (activity-sector-specific responses), where I set nullable to True, while other required fields are not allowed to be null (nullable=False).

After initializing my database, I set up routing in Flask (@app.route), where I had the '/' route render my main "index.html" file, the '/add-data' route render the form ("form.html"), the '/add' route take data from the form and commit them to the db (only the activity-sector-specific questions are sourced from the form and committed to the db and the rest of the columns are null), the '/dashboard/<name>' route render my user-specific dashboard in "dashboard.html" and calculate for certain values, like the total of all carbon emissions from activities, which are passed to "dashboard.html", and the '/api/data' route gives all the data from the database to the the table in "dashboard.html" to be loaded up using an AJAX request. It is important to note that after form data is collected and submission (on submission), the dashboard route is automatically returned to take the user to their personalized dashboard. 

Additionally, I had to take user form data (answers) and find out the carbon emissions released based on that data, also to be stored in the db. Therefore, I created multiple functions which make 'POST' requests to the Climatiq API where the carbon footprint is automatically calculated for certain activities based on the values for each field (ex: power usage when calculating for emissions due to energy). For the flight, I decided to also integrate the AirportGap API, requesting it to calculate the distance between two airports in miles, as I figured users wouldn't know the flight length off the top of their head.

For formatting the form (setting custom question visibility), I used jQuery(.show() and .hide() methods for specific classes and ids given to form questions), while for the table and the chart on the dashboard I used Charts.js and Datatables.js. For overall styling across all templates, I used Bootstrap 5 to make the website look much cleaner and display info in an neat grid with customizable aesthetics (ex: setting custom background and border colors for cards in the index page) - every component on all my pages are cards that take up specific columns in the Bootstrap grid (4, 6, or 12), placed in a row with line breaks between each row. 

To display dashboard stats (totals, chart, etc.), I first summed the total CO2 emissions overall, filtering to only sum CO2 for people whose name matches the name given to the function (name of the current user, filter_by(name=name)), and rounded that value to 2 decimal places, passing this to my render function as a variable to be called in "dashboard.html" ({{ total }}). Then, summed the total carbon emissions for each activity type (query(Profile.activity, func.sum(Profile.co2e))), filtering to sum only have rows with the right name, and grouping the totals by the activity type using group_by() (ex: [("Electricity", 32.56), ("Flight", 150.2)]). I then converted that list of tuples to a dictionary (tba_dict), with keys being the activity type and values being the rounded total for that activity, which I passed to my render function. To create my bar chart, I took this dictionary and converted it to JSON, parsing the data and setting the keys (activity type) to be the chart labels and values to be the chart data. Finally, I counted the number of times a user completed a specific activity type (query(Profile.activity, func.counts(Profile.activity))), filtering to sum only have rows with the right name, grouping the totals by the activity type using group_by() (ex: [("Transportation", 3), ("Flight", 1)]), and then converted that list of tuples to a dictionary which I passed to my render function as well. 

Finally, for my table, I had it be empty initially and then loaded data up when the document was ready using an AJAX request to '/api/data', with my columns being the value in the converted dictionary representing my db (see to_dict()  function); for certain values, I used custom rendering for table values, displaying a certain str with my variables if the db field was null and a different string if it was not null. I formatted my table with the table-striped class and used default DataTables.js styling.

Overall, I used template inheritance for all my pages, with the form, dashboard, and index all extending my base.html file which sourced all my dependencies and the various packages I used throughout (Bootstrap, DataTables).

## Struggles and Learning Points
I did struggle a lot during this project, as this was my first project doing a lot of things. First of all, this was my first project:
- making a website with a back-end on a server
- using and routing flask and the flask structure (templates, static)
- making and using a database (and learning how to use classes and objects in Python)
- using SQL queries and commands and really, just using a database in general (committing, querying, etc.)
- making a form in HTML and sending that data to another place
- getting data from an HTML form with a POST request
- getting data from a Python file and using it in an HTML file ({{}} notation was completely new)
- creating a table in HTML
- using Charts.js and DataTables.js
- using Bootstrap for styling, using jQuery for question visibility
- using the template inheritance structure & blocks
- making and using AJAX requests
- making API requests in Python.

So, naturally, I faced some issues and redirected a lot of times:
- first, I was accessing and manipulating form data in a JS file, which I was going to use to get data to commit into Google Firebase; I realized quickly that it was too much work, I had no idea what I was doing on the Firebase side, and I had issues accessing responses to specific form questions
- then, I found Flask and set up Flask, but had issues accessing form responses in my Flask request and committing them to a database (it turns out I never gave my user input tags a name, so Flask couldn't pick up any of them; but it took a bit of trial and error for me to realize that)
- I created an initialize_db() and never actually called it at one point, giving me issues
- I used a virtual environment in this project, and I had trouble getting the venv to be active the first time around (when importing my modules, I kept getting ModuleNotFound errors even though I had installed them earlier) - the fix turned out to be deleting my venv and creating a new one
- my database didn't render in table form in my HTML document, because I had formatting issues nesting the tr and th tags
- when making an API request to find the carbon footprint of an activity, I first was using the Carbon Interface API, but that API turned out to be inactive (or just unusable - I'm not sure), so I switched to Climatiq for my calculations and changed the structure of my request
- when changing question visibility, I first was using my static js file to change it, which didn't work great to remove spacing taken up by questions not shown, so I ended up switching to jQuery when changing my visibility
- I never had a catch-all return redirect() statement after committing to my database at some point, so I kept getting an error
- there were also several times where I would change the structure of my db (adding columns), and keep my original instance (site.db file), which led to internal server errors at some points
- finally, when displaying info on my dashboard page, I was summing the CO2 emissions data when it was a string, not a float, and I was not rounding it, leading to errors and float precision errors; then, once I changed my CO2 emission value to a float, I never stored it as that in my database, and so naturally I did not get an accurate value for CO2 emission sums by activity type.
For the scope of the project, I do think I was able to avoid making a lot of mistakes due to my copious usage of print() statements in my code and some very, very helpful materials including tutorials on how to build a Flask database, descriptions of what SQL commands are and how to use them, tutorials on AJAX requests and creating a table using DataTables.js, the documentation for Bootstrap, descriptions of how template inheritance works, and so much more. 

From the mistakes I did make, I was also able to gain a better understanding of Flask and database structure, Bootstrap and HTML/CSS in general (I had no idea a tag could have more than one class, for example!), and so much more!

## Notes on Usage & Other 
Quick notes on usage: please, when filling out the form, fill out all the fields you see, and DO NOT specify units!! This is especially important, as several of my fields require a numerical input of some kind and will break if you input a string like "50 mi". Additionally, I only have 250 free API credits/month on Climatiq, so please do keep that in mind.


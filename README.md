# Data-Driven Web App
This is a data-driven web app built with Flask. The app uses a SQLite database to store data about movies and actors.

# Dependencies
The app requires the following dependencies:

 - Flask
 - render_template
 - SQLAlchemy
 - flask_sqlalchemy
You can install these dependencies using the pip install command.

# Data Source
For this app, data was obtained from Kaggle.com. They provided a .csv file which contained data on movies and actors. This data was then loaded into a SQLite database named movies.db.

# Features
The app has the following features:

Displays a list of all movies on the homepage.
Allows users to view details about a particular movie by clicking on its title.
Displays a list of all actors on a separate page.
Implements error handling to handle 404 errors.

# Testing
The app includes a test file named test_app.py which contains test cases for the app's features. You can run the tests using the following command:

`python -m unittest test_app.py`

# How to Run the App
To run the app, execute the following command:


`python app.py`
Then, open your web browser and go to http://localhost:5000/ to view the app.





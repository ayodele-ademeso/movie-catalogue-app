# Movie Catalog Application

This is a simple Flask application that allows you to manage a catalog of movies. You can add new movies, search for movies by name, and retrieve a list of all movies.

## Requirements

- Python 3.x
- Flask
- Boto3

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/ayodele-ademeso/movie-catalogue-app.git
   cd movie-catalog-app

2. Create a virtual environment:

    ```bash
    python -m venv venv

3. Activate the virtual environment

- On Windows:
    venv\Scripts\activate

- On Unix or MacOS:
    ```bash
    source venv/bin/activate

4. Install dependencies

    ```bash
    pip install -r requirements.txt

5. Set Environment variables

    ```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development

6. Run app

    ```bash
    flask run

    Visit http://localhost:5000 in your browser.

## Routes
    /: Home page with a form to add new movies.
    /get_movie/<movie_name>: Search for movies by name.
    /get_all_movies: Retrieve a list of all movies.


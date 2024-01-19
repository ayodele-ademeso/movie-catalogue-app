# Movie Catalog Application

This is a simple Flask application that allows you to manage a catalog of movies. You can add new movies, search for movies by name, and retrieve a list of all movies.

## Requirements

- Python 3.x
- Python Venv
- Flask
- Boto3

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/ayodele-ademeso/movie-catalogue-app.git
   cd movie-catalogue-app

2. Create a virtual environment:

    ```bash
    python3 -m venv venv

3. Activate the virtual environment

- On Windows:
    ```bash
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
    flask run --host='0.0.0.0'

    Visit http://localhost:5000 in your browser.

## Routes
The following routes are available on this API:

    ```bash
    /: API's homepage.
    /health: Checks the health status of the application
    /api/movies: Accepts either a GET request(to get all movies), or a POST request(for adding movies).
    /api/search: Returns a movie or list of movies if search parameter matches.
    /api/movies/<title>: Accepts a PUT method for updating details of a single movie


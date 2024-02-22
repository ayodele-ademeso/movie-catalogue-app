# Movie Catalogue Application

This is a simple Flask application that allows you to manage a catalogue of movies. You can add new movies, search for movies by name, and retrieve a list of all movies.

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

2. Build the image with Docker:

    ```bash
    docker build -t movie-library:{$TAG} .

3. Run the docker image

    ```bash
    docker run --env-file <path/to/your/.env/file> -it movie-library:{$TAG}

4. Test application

    ```bash
    curl http://localhost:8000

## Routes
The following routes are available on this API:

    /: API's homepage.
    /health: Checks the health status of the application.
    /api/movies: Accepts either a GET request(to get all movies), or a POST request(for adding movies).
    /api/search: Returns a movie or list of movies if search parameter matches.
    /api/movies/<title>: Accepts a PUT method for updating details of a single movie.


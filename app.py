from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import csv
import boto3
from botocore.exceptions import NoCredentialsError
from io import StringIO

app = Flask(__name__)
CORS(app)

# Retrieve environment variables
AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME', 'ayodele-csv-bucket')
AWS_CSV_FILE_KEY = os.environ.get('AWS_CSV_FILE_KEY', 'movies.csv')


def check_and_create_csv():
    # Initialize S3 client
    s3 = boto3.client('s3')
    try:
        # Check if the CSV file exists in the S3 bucket
        s3.head_object(Bucket=AWS_BUCKET_NAME, Key=AWS_CSV_FILE_KEY)
    except NoCredentialsError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        csv_data = StringIO()
        csv_writer = csv.DictWriter(csv_data, fieldnames=["Title", "Year", "Genre", "Rating"])
        csv_writer.writeheader()
        try:
            s3.put_object(Body=csv_data.getvalue(), Bucket=AWS_BUCKET_NAME, Key=AWS_CSV_FILE_KEY)
        except Exception as create_error:
            print(f"Error creating CSV file: {create_error}")
            return False

        return True

# Check and create the CSV file in S3
check_and_create_csv()

def read_movies():
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=AWS_BUCKET_NAME, Key=AWS_CSV_FILE_KEY)
        movies_data = list(csv.DictReader(response['Body'].read().decode('utf-8').splitlines()))
        return movies_data
    except NoCredentialsError as e:
        return {"error": f"Error reading movies from S3: {e}"}

def is_duplicate(existing_titles, new_title):
    return any(title.lower() == new_title.lower() for title in existing_titles)

def write_movies(movie):
    s3 = boto3.client('s3')

    try:
        # Read the existing content of the CSV file
        response = s3.get_object(Bucket=AWS_BUCKET_NAME, Key=AWS_CSV_FILE_KEY)
        existing_data = response['Body'].read().decode('utf-8')

        # Convert the existing data to a list of dictionaries
        existing_movies = list(csv.DictReader(StringIO(existing_data), fieldnames=["Title", "Year", "Genre", "Rating"]))

        # Extract existing movie titles for duplicate check
        existing_titles = [existing_movie["Title"] for existing_movie in existing_movies]

        # Check for duplicates before adding
        if is_duplicate(existing_titles, movie["Title"]):
            return {"error": f"Duplicate movie: {movie['Title']}"}, 409  # Conflict

        # Convert the new movie dictionary to a CSV-formatted string
        csv_data = StringIO()
        csv_writer = csv.DictWriter(csv_data, fieldnames=["Title", "Year", "Genre", "Rating"])
        csv_writer.writerow(movie)
        new_movie_data = csv_data.getvalue().strip()

        # Append the new movie data to the existing content
        new_data = f"{existing_data}\n{new_movie_data}"

        # Upload the updated content back to S3
        s3.put_object(Bucket=AWS_BUCKET_NAME, Key=AWS_CSV_FILE_KEY, Body=new_data)

        return {"message": "Movie added successfully"}, 201

    except NoCredentialsError as e:
        return {"error": f"Error writing movie to S3: {e}"}, 500  # Internal Server Error
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}, 500  # Internal Server Error

def search_movies(keyword):
    keyword_lower = keyword.lower()
    movies_data = read_movies()
    matching_movies = [movie for movie in movies_data if keyword_lower in movie['Title'].lower()]
    return matching_movies

def update_movie(title, update_data):
    movies = read_movies()

    if not isinstance(movies, list):
        print("Error: 'read_movies' did not return a list.")
        return False

    # Find the index of the movie with the specified title
    index = next((i for i, movie in enumerate(movies) if movie.get('Title', '').lower() == title.lower()), None)

    if index is not None:
        # Update the movie with the new data
        movies[index].update(update_data)

        # Write the updated data back to the CSV file in S3
        write_movies(movies)

        return True  # Movie updated successfully
    else:
        print(f"Error: Movie with title '{title}' not found.")
        return False  # Movie not found

@app.route('/health', methods=['GET'])
def health():
    """Check the status of this application."""
    return ';-)'

@app.route('/')
def index():
    return "Movies API"

@app.route('/api/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'GET':
        movies_data = read_movies()
        return jsonify(movies_data)

    elif request.method == 'POST':
        movie_data = request.json
        result, status_code = write_movies(movie_data)

        if status_code == 409:
            return jsonify({"message": result["error"]}), 409  # Conflict
        elif status_code == 500:
            return jsonify({"message": result["error"]}), 500  # Internal Server Error
        else:
            return jsonify(result), status_code


@app.route('/api/search', methods=['GET'])
def search():
    keyword = request.args.get('q', '')
    matching_movies = search_movies(keyword)

    if matching_movies:
        return jsonify(matching_movies)
    else:
        return jsonify({"message": "Movie Not Found"}), 404

@app.route('/api/movies/<title>', methods=['PUT'])
def update_movie_endpoint(title):
    try:
        update_data = request.json

        # Check if update_data is a dictionary and contains valid fields
        if not isinstance(update_data, dict) or not any(field in update_data for field in ['Year', 'Genre', 'Rating']):
            return jsonify({"message": "Invalid update data"}), 400  # Bad Request

        if update_movie(title, update_data):
            return jsonify({"message": "Movie updated successfully"}), 200
        else:
            return jsonify({"message": "Movie not found"}), 404

    except Exception as e:
        return jsonify({"message": f"Error updating movie: {str(e)}"}), 500  # Internal Server Error

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
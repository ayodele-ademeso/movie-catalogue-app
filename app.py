import os
import boto3
from flask import Flask, render_template, request, redirect, url_for, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# DYNAMODB_TABLE = os.getenv('DYNAMODB_TABLE')
# dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION'))
DYNAMODB_TABLE = "movie-catalogue-db"
dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
table = dynamodb.Table(DYNAMODB_TABLE)

@app.route('/')
def index():
    return render_template('index.html')

def get_last_movie_id():
    response = table.scan(
        ProjectionExpression='id',
        Limit=1,
    )
    last_movie = response.get('Items', [])
    return int(last_movie[0]['id']) if last_movie else 0

def get_next_movie_id():
    return get_last_movie_id() + 1

@app.route('/add_movie', methods=['POST'])
def add_movie():
    title = request.form['title']
    genre = request.form['genre']
    year = request.form['year']
    rating = request.form['rating']
    movie_id = get_next_movie_id()

    # If no similar movie found, add the new movie with an incremental ID
    table.put_item(
        Item={
            'id': movie_id,
            'title': title,
            'genre': genre,
            'year': int(year),
            'rating': rating
        }
    )

    # return redirect(url_for('index'))
    return redirect(url_for('get_all_movies'))

@app.route('/get_all_movies', methods=['GET'])
def get_all_movies():
    movies = []

    response = table.scan()
    movies = response.get('Items', [])

    return jsonify(movies)

@app.route('/get_movie/<movie_name>', methods=['GET'])
def get_movie(movie_name):
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('title').eq(movie_name)
    )

    movies = response.get('Items', [])

    return jsonify(movies)
    return render_template('search.html', movies=movies)

# def lambda_handler(event, context):
#     return app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

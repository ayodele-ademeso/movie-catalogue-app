import csv
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
CSV_FILE = "movies.csv"

def create_csv():
    with open(CSV_FILE, 'a', newline='') as csvfile:
        fieldnames = ['id', 'title', 'genre', 'year', 'rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

# Retrieve the last movie ID from the CSV file
def get_last_movie_id():
    with open(CSV_FILE, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        last_movie = list(reader)[-1]
        return int(last_movie['id']) if 'id' in last_movie else 0

# Get the next movie ID by incrementing the last movie ID
def get_next_movie_id():
    return get_last_movie_id() + 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_movie', methods=['POST'])
def add_movie():
    title = request.form['title']
    genre = request.form['genre']
    year = request.form['year']
    rating = request.form['rating']

    # Get the next movie ID
    movie_id = get_next_movie_id()

    with open(CSV_FILE, 'a', newline='') as csvfile:
        fieldnames = ['id', 'title', 'genre', 'year', 'rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write the header if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow({'id': movie_id, 'title': title.title(), 'genre': genre.title(), 'year': year, 'rating': float(rating)})

    return redirect(url_for('index'))

@app.route('/get_all_movies', methods=['GET'])
def get_all_movies():
    movies = []

    with open(CSV_FILE, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        movies = list(reader)

    return jsonify(movies)

@app.route('/get_movie', methods=['GET'])
def search_movie():
    movie_name = request.args.get('movie_name')
    
    if not movie_name:
        return "Please provide a movie name for search."

    movies = []
    with open(CSV_FILE, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if movie_name.lower() in row['title'].lower():
                movies.append(row)

    return render_template('search.html', movies=movies)

if __name__ == '__main__':
    create_csv()
    app.run(debug=True, host='0.0.0.0')

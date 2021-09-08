from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from movie import Movie
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# creates application
app = Flask(__name__)
Bootstrap(app)

# creates database
try:
    cred = credentials.Certificate(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    firebase_admin.initialize_app(cred)
except KeyError:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'movies-collection-324718',
    })

db = firestore.client()
collection = db.collection('movies')


def add_record(movie):
    # method to add a new record using Movie class
    new_record = collection.document(f'{movie.name.replace(" ", "")}')
    new_record.set({
        'name': movie.name,
        'genre': movie.genres,
        'rating': float(movie.rating),
        'description': movie.description,
        'actors': movie.actors,
        'duration': movie.duration,
        'url': movie.url,
        'image': movie.image
    })


@app.route('/')
def home():
    # Retrieves data from database and loading home.html page
    query = collection.order_by('rating', direction=firestore.Query.DESCENDING)
    movies_documents = query.stream()
    movies_collection = [doc.to_dict() for doc in movies_documents]
    print(movies_collection)
    return render_template('home.html', collection=movies_collection)


@app.route('/add', methods=["GET", "POST"])
def add():
    # catches new movie url from the form input
    if request.method == "POST":
        url = request.form["link"]
        # removes parameters after redirecting from another IMDB page
        if "?" in url:
            position = url.index("?")
            url = url.replace(url[position:], "")
        # handling exceptions:
        try:
            # adds new movie to the database
            new_movie = Movie(url)
            add_record(new_movie)
            return redirect(url_for('home'))
        except TypeError:
            return redirect(url_for('home', response="Could not retrieve info from provided link."))
        except requests.exceptions.MissingSchema:
            return redirect(url_for('home', response="Please provide a valid url."))


@app.route("/remove")
def remove():
    # removes a movies from the database and website
    movie_to_delete = request.args.get('name')
    collection.document(f'{movie_to_delete}').delete()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)


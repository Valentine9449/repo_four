import sqlite3

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\Hillel\Hillel 5\data.db'
app.config['SECRET_KEY'] = 'aaaaaadswssds'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

conn = sqlite3.connect('sqlite_test.db')
c = conn.cursor()


class Actor(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    surname = db.Column(db.String(80), unique=True, nullable=False)
    year_of_birth = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<actor: {self.pk}>"


class Movie(db.Model):
    pk = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(80), unique=True, nullable=False)
    year = db.Column(db.String(120), unique=True, nullable=False)
    genre = db.Column(db.String(120), unique=True, nullable=False)
    rating = db.Column(db.Integer, unique=True, nullable=False)

    actor_surname = db.Column(db.Integer, db.ForeignKey('actor.surname'))

    def __repr__(self):
        return f"<movie: {self.title}>"


class Genre(db.Model):
    pk = db.Column(db.Integer, primary_key=True)

    movie_name = db.Column(db.String(100), db.ForeignKey('movie.title'))
    movie_genre = db.Column(db.String(100), db.ForeignKey('movie.genre'))

    def __repr__(self):
        return f"<genre: {self.pk}>"


@app.route('/')
def main():
    return 'Hello'


@app.route('/set_movies', methods=['POST', 'GET'])
def set_movie():
    if request.method == 'POST':
        try:
            actor = Actor(name=request.form['name'], surname=request.form['surname'],
                          year_of_birth=request.form['year'])
            db.session.add(actor)

            movie = Movie(title=request.form['title'], year=request.form['year'],
                          genre=request.form['genre'], rating=request.form['rating'],
                          actor_surname=actor.surname)
            db.session.add(movie)

            genre = Genre(movie_name=movie.title, movie_genre=movie.genre)
            db.session.add(genre)
            db.session.commit()

        except:
            db.session.rollback()
            print("Error")

    return render_template('add_movies.html')


@app.route('/movies', methods=['GET'])
def show_movie():
    movies = []
    try:
        movies = Movie.query.all()
    except:
        print("Error")

    return render_template('index.html', data=movies)


if __name__ == '__main__':
    app.run(debug=True)

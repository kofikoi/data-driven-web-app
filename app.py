from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    movies = db.relationship('Movie', backref='actor', lazy=True)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable=False)



def load_data():
    with open('movies.csv') as f:
        reader = csv.reader(f)
        next(reader) # skip the header row
        for row in reader:
            # Create an Actor object for each actor in the row
            actors = []
            for actor_name in row[2].split(','):
                actor = Actor(name=actor_name.strip())
                db.session.add(actor)
                actors.append(actor)

            # Create a Movie object for the row, linking it to the actors
            movie = Movie(title=row[0], year=row[1])
            movie.actors = actors
            db.session.add(movie)

    db.session.commit()


@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

# Create the database and load the data
if __name__ == '__main__':
    db.create_all()
    load_data()
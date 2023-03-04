import csv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(app)

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Actor %r>' % self.name

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    actors = db.relationship('Actor', secondary='movie_actor', backref=db.backref('movies', lazy='dynamic'))

    def __repr__(self):
        return '<Movie %r>' % self.title

class MovieActor(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), primary_key=True)

    def __repr__(self):
        return '<MovieActor %r-%r>' % (self.movie_id, self.actor_id)



def load_data():
    with open('movies.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader) # skip the header row
        count = 0
        for row in reader:
            # Create an Actor object for each actor in the row
            actors = []
            for actor_name in row[2].split(','):
                try:
                    actor = Actor(name=actor_name.strip())
                    db.session.add(actor)
                    actors.append(actor)
                except IntegrityError:
                    db.session.rollback()
                    continue

            # Create a Movie object for the row, linking it to the actors
            movie = Movie(title=row[0], year=row[1])
            movie.actors = actors
            db.session.add(movie)
            try:
                db.session.commit()
                count += 1
            except IntegrityError:
                db.session.rollback()
        print(f"{count} records were added to the database")



@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/actors')
def actors():
    actors = Actor.query.all()
    return render_template('actors.html', actors=actors)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get(movie_id)
    return render_template('movie.html', movie=movie)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        load_data()
    app.run(debug=True)



from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_flask.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

db.init_app(app)

class Movie(db.Model):
    __tablename__ = "movies"
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False, unique=True)
    title_en = db.Column(db.String, nullable=False)
    audience = db.Column(db.Integer, nullable=False)
    open_date = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    watch_grade = db.Column(db.String, nullable=False)
    score = db.Column(db.Float, nullable=False)
    poster_url = db.Column(db.TEXT, nullable=False)
    description = db.Column(db.TEXT, nullable=False)
    
db.create_all()

@app.route("/")
def root():
    return redirect("/movies/")

@app.route("/movies/")
def index():

    data = Movie.query.all()

    return render_template("index.html",data=data)


@app.route("/movies/new/")
def new():
    
    return render_template("new.html")

@app.route("/movies/create/", methods=["POST"])
def create():
    title = request.form.get("title")
    title_en = request.form.get("title_en")
    audience = request.form.get("audience")
    open_date = request.form.get("open_date")
    genre = request.form.get("genre")
    watch_grade = request.form.get("watch_grade")
    score = request.form.get("score")
    poster_url = request.form.get("poster_url")
    description = request.form.get("description")
    
    record = Movie(title=title, title_en=title_en, audience=audience,
    open_date=open_date,genre=genre,watch_grade=watch_grade,score=score,poster_url=poster_url,
    description=description)

    db.session.add(record)
    db.session.commit()

    return redirect("/movies/")# => /movies/{number}



@app.route("/movies/<int:pid>/")
def show(pid):
    data = Movie.query.get(pid)
    return render_template("show.html", data=data)


@app.route("/movies/<int:pid>/edit/")
def edit(pid):
    
    
    data = Movie.query.get(pid)

    return render_template("edit.html", data=data)


@app.route("/movies/<int:pid>/update/", methods=["POST"])
def update(pid):
    D = get_post()
    data = Movie.query.get(pid)
    data.title = D['title']
    data.title_en = D['title_en']
    data.audience = D['audience']
    data.open_date = D['open_date']
    data.genre = D['genre']
    data.watch_grade = D['watch_grade']
    data.score = D['score']
    data.poster_url = D['poster_url']
    data.description = D['description']
    
    db.session.commit()
    
    return redirect("/movies/{}/".format(data.id))


@app.route("/movies/<int:pid>/delete/")
def delete(pid):
    data = Movie.query.get(pid)
    db.session.delete(data)
    db.session.commit()
    
    return redirect("/movies/")




def get_post():
    D={}
    D['title'] = request.form.get("title")
    D['title_en'] = request.form.get("title_en")
    D['audience'] = request.form.get("audience")
    D['open_date'] = request.form.get("open_date")
    D['genre'] = request.form.get("genre")
    D['watch_grade'] = request.form.get("watch_grade")
    D['score'] = request.form.get("score")
    D['poster_url'] = request.form.get("poster_url")
    D['description'] = request.form.get("description")
    return D
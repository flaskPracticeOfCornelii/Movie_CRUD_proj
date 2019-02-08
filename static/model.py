from ops import MovieCollector
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy


mc = MovieCollector()
# mc.make_csv_files()
# mc.gathering_info(2019,1,13)

mc.update_by_csv()



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db_flask.sqlite3'
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

for key,value in mc.movie_info.items():
    
    pid = key
    title = value[0]
    title_en = value[1]
    audience = mc.boxoffice[key][1]
    open_date = "20000101"
    genre = value[5]
    watch_grade = value[7]
    score = 4.5
    poster_url = "0"
    for url in mc.imgs:
        if key == url[0]:
            poster_url = url[1]
    description = "Not yet"
    record = Movie(id=key, title=title, title_en=title_en, audience=audience,
        open_date=open_date,genre=genre,watch_grade=watch_grade,score=score,poster_url=poster_url,
        description=description)
    db.session.add(record)
    
db.session.commit()
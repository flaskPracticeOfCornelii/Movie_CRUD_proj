# CRUD Project
1. flask를 활용하였다.
2. base.html에 필요한 Font와 Bootstrap의 link를 head에 넣고 body에 header와 footer를 구현하여
다른 html문서에서 상속하는 위 문서를 상속하는 형식으로 구현하였다. 
3. C9환경에서 구현하였다.

## I. 데이터베이스
아래와 같이 flask_sqlalchemy을 통해 ORM을 활용하였다.

```python
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

```
## II. 페이지
#### 1. 영화목록 
1. 접근 페이지를 `/movies/`로 하기 위해서
아래와 같이 `/`에서는 `/movies/`로 redirection시켰다.

```python
@app.route("/")
def root():
    return redirect("/movies/")
```

또 아래와 같이 적절한 메소드를 통해 DB에 있는 전체 정보를 긁어와서 해당 html문서로 넘겼다.

```python
@app.route("/movies/")
def index():
    data = Movie.query.all()
    return render_template("index.html",data=data)
```

2. `/movies` 페이지에는 title, score를 볼 수 있도록 구현하였다.

3. 위 해당 정보를 담은 box 클릭할 시 영화 정보 조회로 넘어가도록 하였다.

4. a링크를 활용하여, 영화 정보 생성으로 이동할 수 있도록 하였다.

5. 위 title, score와 함께 포스터 이미지를 볼 수 있도록 하였으며,
6. 전체적으로 bootstrap을 활용하여 만들었다.
7. Base.html을 jinja syntax를 통해 상속하여 코드를 간결화하였다.


#### 2. 영화정보생성 (new)
1. `/movies/new/' html으로 넘겨주도록 구현하였다.
2. 요구되는 필드명과 input type에 맞춰 구현하였다.
3. 영화정보올리기 버튼을 통해 FORM 태그의 정보가 `/movies/create/` 로 넘어가도록 하였다.
4. POST 방식을 사용하였다.
5. score는 input의 속성에서 `min=0 max=5 step=0.5`을 적용하였다.


#### 3. 영화정보생성 (create)
1. 아래와 같이 /movies/create/ 의 함수를 선언하였다.
2. flask_sqlalchemy object가 가진 메소듣 활용하여 db에 저장하였다.
3. 영화 정보 조회로 redirect 시켰다.

```python
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
```
#### 4. 영화정보조회 (show)
1. `<int:pid>`와 같이 라우팅변수를 활용하여 DB의 키를 받아올 수 있도록 하였다.
2. .query.get(pid)을 활용하여 해당 영화의 정보를 불러와서 show.html로 넘겨주었다.
3. 목록으로 돌아가기, 수정, 삭제를 a링크의 형식에 id를 라우팅변수 형태로 넘겨주도록 하였다.

```python
@app.route("/movies/<int:pid>/")
def show(pid):
    data = Movie.query.get(pid)
    return render_template("show.html", data=data)
```

#### 5. 영화 정보 수정 (edit)
1. `/movies/<int:pid>/edit`와 같이 라우팅변수를 활용하여 DB의 키를 받아올 수 있도록 하였다.
2. 넘겨받은 정보를 속성 value= 에 넣어주거나, bootstrap의 textarea같은 경우 <>{}<> 태그 사이에 넣어서 표시해 주었다.
3. FORM 태그 내에서 해당 사항들을 구현하였다.
4. POST형식을 사용하였다.

```python

@app.route("/movies/<int:pid>/edit/")
def edit(pid):
    
    data = Movie.query.get(pid)
    return render_template("edit.html", data=data)

```

#### 6. 영화 정보 수정 (update)
1. `/movies/<int:pid>/update`와 같이 라우팅변수를 활용하여 DB의 키를 받아올 수 있도록 하였다.
2. 아래와 같이 해당 id의 레코드를 불러와서 저장된 값들을 모두 수정한 뒤 커밋하였다.
3. 영화정보조회 페이지로 redirect시켰다.

```python
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

```
#### 7. 영화 정보 삭제 (delete)
1. `/movies/<int:pid>/delete`와 같이 라우팅변수를 활용하여 DB의 키를 받아올 수 있도록 하였다.
2. 아래와 같이 삭제하였다.
3. 영화정보목록으로 redirect하였다.

```python

@app.route("/movies/<int:pid>/delete/")
def delete(pid):
    data = Movie.query.get(pid)
    db.session.delete(data)
    db.session.commit()
    
    return redirect("/movies/")

```
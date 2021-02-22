from flask import Flask , render_template , request , redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from datetime import datetime
from fuzzywuzzy import fuzz
import Levenshtein as lev
import numpy as np

app = Flask(__name__)

app.config [ 'SQLALCHEMY_DATABASE_URI' ] = 'postgresql://postgres:123456@localhost/postgres'

db = SQLAlchemy(app)

# class bbc(db.Model):
#     bbc_id= db.column(db.Serial, Primary_key= True)
#     bbc_date=db.column(db.String(255))
#     bbc_time=db.column(db.Time)
#     bbc_published=db.column(db.String(255))
#     bbc_title=db.column(db.String(255))
#     bbc_link=db.column(db.String(255))
#     bbc_summuary=db.column(db.Text)

# bbc = db.Table('bbc',db.metadata,autoload=True, autoload_with=db.engine)

Base = automap_base( )
Base.prepare(db.engine , reflect=True)
news = Base.classes.news


@app.route('/', )
def index():
    # results = db.session.query(news).order_by(news.id.desc( )).all( )
    # return render_template('index.html' , news=results)
    return  render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post/<int:id>')
def post(id):
    post = db.session.query(news).filter_by(id=id).first( )
    return render_template('post.html' , post=post)


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/add' , methods=[ 'POST' ])
def getvalue():
    firsttitle = request.form [ 'title' ]
    secondtitle = request.form [ 'compared_title' ]
    return render_template('add.html')


@app.route('/addpost' , methods=[ 'POST' ])
def addpost():
    title = request.form [ 'title' ]
    compared_title = request.form [ 'compared_title' ]
    Str1 = title.tostring
    Str2 = compared_title.tostring
    Ratio = fuzz.ratio(Str1.lower( ) , Str2.lower( ))
    Partial_Ratio = fuzz.partial_ratio(Str1.lower( ) , Str2.lower( ))
    Token_Sort_Ratio = fuzz.token_sort_ratio(Str1 , Str2)
    Token_Set_Ratio = fuzz.token_set_ratio(Str1 , Str2)
    print(Ratio)
    print(Partial_Ratio)
    print(Token_Sort_Ratio)
    print(Token_Set_Ratio)


if __name__ == '__main__':
    app.run(debug=True)
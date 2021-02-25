from flask import Flask , render_template , request , redirect , url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from sqlalchemy.ext.automap import automap_base
from datetime import datetime
from fuzzywuzzy import fuzz
import Levenshtein as lev
import numpy as np
import openpyxl
import pandas as pd
from os import path
from PIL import Image
import psycopg2
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import csv
import matplotlib.pyplot as plt
import sqlalchemy as sq
import string
import xlwt
import xlsxwriter
import pandas.io.sql
from openpyxl import Workbook


app = Flask(__name__)

app.config [ 'SQLALCHEMY_DATABASE_URI' ] = 'postgresql://postgres:123456@localhost/postgres'
# POSTGRESQL_URI = "postgresql://postgres:123456@localhost/postgres"

db = SQLAlchemy(app)
# connection = psycopg2.connect(POSTGRESQL_URI)




# class bbc(db.Model):
#     bbc_id= db.column(db.Serial, Primary_key= True)
#     bbc_date=db.column(db.String(255))
#     bbc_time=db.column(db.Time)
#     bbc_published=db.column(db.String(255))
#     bbc_title=db.column(db.String(255))
#     bbc_link=db.column(db.String(255))
#     bbc_summuary=db.column(db.Text)

# bbc = db.Table('bbc',db.metadata,autoload=True, autoload_with=db.engine)
news = db.Table('news',db.metadata, autoload= True, autoload_with = db.engine)

# Base = automap_base( )
# Base.prepare(db.engine , reflect=True)
# news = Base.classes.bbc
connection = psycopg2.connect(user="postgres" ,
                              password="123456" ,
                              host="127.0.0.1" ,
                              port="5432" ,
                              database="postgres")
cursor = connection.cursor()

now = datetime.now ( )
current_date = now.strftime ( "%a, %d %B, %Y %H:%M:%S")
current_time= now.strftime ( "%H:%M:%S" )
current_date_2 = now.strftime("%Y-%m-%d")

def usernumber():
    numbers = [ ]
    f = open("numbers.txt" , "r")
    for line in f.read( ).splitlines( ):
        if line != "":
            numbers.append(line)
    f.close( )
    total_number = len(numbers)
    return total_number


@app.route('/', )
def index():
    # results = db.session.query(news).order_by(news.id.desc( )).all( )
    total_number = usernumber( )
    return render_template('index.html', total_number = total_number)
    # return  render_template('index.html')


@app.route('/news',)
def news():
    # with connection:
    #     with connection.cursor( ) as cursor:
    #         results=cursor.execute("SELECT * FROM news")
    # results = db.session.query(news).order_by(news.id.desc( )).all( )
    # return render_template('index.html' , news=results)


    fetch_query = ('SELECT * FROM NEWS')
    cursor.execute (fetch_query)

    # print ( "Selecting rows from mobile table using cursor.fetchall" )
    mobile_records = cursor.fetchall ( )

    return render_template('news.html', news = mobile_records, current_date = current_date)


@app.route('/track')
def track():
    current_date_string = str(current_date_2)
    postgreSQL_select_Query = ("select * from dummy where dummy_date='%s'" % current_date_string)

    cursor.execute(postgreSQL_select_Query)
    mobile_records = cursor.fetchall( )
    todays_news = len(mobile_records)

    current_date_string = str(current_date_2)
    postgreSQL_select_Query = ("select dummy_time from dummy where dummy_date='%s' order by dummy_id desc" % current_date_string)

    cursor.execute(postgreSQL_select_Query)
    mobile_records2 = cursor.fetchall()
    last_fetch_news = mobile_records2[0]

    str(last_fetch_news)






    total_number = usernumber()
    return render_template('track.html', current_date = current_date,total_numbers= total_number,todays_news=todays_news,last_fetch_news=last_fetch_news)


@app.route('/pages')
def pages():
    return render_template('pages.html')

@app.route('/charts')
def charts():
    the_frame = pd.read_sql("SELECT * FROM news" , connection)

    comment_words = ''
    stopwords = set(STOPWORDS)


    for val in the_frame.title:

        val = str(val)


        tokens = val.split( )


        for i in range(len(tokens)):
            tokens [ i ] = tokens [ i ].lower( )

        comment_words += " ".join(tokens) + " "

    wordcloud = WordCloud(width=800 , height=800 ,
                          background_color='white' ,
                          stopwords=stopwords ,
                          min_font_size=10).generate(comment_words)

    # plot the WordCloud image
    plt.figure(figsize=(8 , 8) , facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.savefig('static/img/fool.png' , bbox_inches='tight')

    return render_template('charts.html', current_date = current_date)

@app.route('/tables')
def tables():
    cursor = connection.cursor()

    fetch_query = ('SELECT * FROM NEWS')
    cursor.execute (fetch_query)
    # print ( "Selecting rows from mobile table using cursor.fetchall" )
    mobile_records = cursor.fetchall ( )
    return render_template('tables.html',news=mobile_records )


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')

@app.route('/error')
def error():
    return render_template('404.html')

@app.route('/blank_page')
def blank():
    return render_template('blank.html')


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

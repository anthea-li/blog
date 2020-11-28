from flask import Flask, render_template, redirect, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://antheali:@localhost:5432/demo'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(100))
    author = db.Column(db.String(100))
    date_posted = db.Column('date_posted', db.DateTime, default=datetime.now())
    content = db.Column(db.String(1000))

@app.route('/')
def index():
    blog_posts = BlogPost.query.all()
    return render_template('index.html', posts=blog_posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def add_post():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    new_post = BlogPost(
        title = title, 
        subtitle = subtitle, 
        author = author, 
        date_posted = datetime.now(),
        content = content)

    db.session.add(new_post)
    db.session.commit()
    return redirect('/')

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    post = BlogPost.query.get(post_id)
    return render_template('post.html', post=post)

@app.route('/news')
def news():
    url = ('http://newsapi.org/v2/top-headlines?country=us&apiKey=74765868ef0a4fb1845d710f10ed5293')
    response = requests.get(url)
    data = response.json()
    return str(data)

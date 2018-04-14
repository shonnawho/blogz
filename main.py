from flask import Flask, redirect, render_template, request
import os
import jinja2
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True


db = SQLAlchemy(app)


#class for database
class Blog(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self,title,body):
        self.title = title
        self.body = body


    





@app.route('/newpost', methods=['POST','GET'])
def newpost():

    blog_body= ''
    blog_title = '' 
    
    if request.method == 'POST':
        blog_body = request.form['blog_body']
        blog_title = request.form['blog_title']

        #blog = [blog_title, blog_body]

    
        return redirect("/blog")
    else:
        
        
        return render_template('newpost.html', title='Blogs', blog_body=blog_body,blog_title=blog_title)









@app.route('/blog', methods=['POST','GET'])
def blog():
    if request.method == 'POST':
        
        blog_body = request.form['blog_body']
        blog_title = request.form['blog_title']
    
        return render_template('blog.html', blog_title=blog_title,blog_body=blog_body)



if __name__ == '__main__':

    app.run()
 
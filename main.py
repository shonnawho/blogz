from flask import Flask, redirect, render_template, request, flash
import os
import jinja2
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 's1i9r8p6'



db = SQLAlchemy(app)

#class for database
class Blog(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self,title,body,blog):
        self.title = title
        self.body = body
        

 @app.route('/')
def index():
    blog_page = request.args.get('')
    return redirect('/blog')
    
@app.route('/newpost', methods=['POST','GET'])
def newpost():

    blog_body= ''
    blog_title = '' 
    
    if request.method == 'POST':

        blog_body = request.form['blog_body']
        blog_title = request.form['blog_title']
        
        return render_template('newpost.html', title='Blogs', blog_body=blog_body,blog_title=blog_title)
        
    else:
        
        
        return render_template('newpost.html', title="Blogs")


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    
    if request.method == 'POST':
        
        blog_body = request.form['blog_body']
        blog_title = request.form['blog_title']
        new_blog = Blog(blog_title, blog_body,blog)
        db.session.add(new_blog)
        db.session.commit()
        #request.args.get('blog_list')

    blog_list = Blog.query.filter_by().all()
    return render_template('blog.html',blog_list=blog_list)
    

if __name__ == '__main__':

    app.run()
 
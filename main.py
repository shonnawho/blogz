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

    def __init__(self,title,body):
        self.title = title
        self.body = body
        

#app.route('/')
#def index():

    #return redirect('/blog')


@app.route('/newpost', methods=['POST','GET'])
def newpost():


    if request.method == 'POST':
        
        blog_body = request.form['blog_body']
        blog_title = request.form['blog_title']
        title_error = ''
        body_error = ''


        if len (blog_body) < 1:
            body_error = 'Must have content!'


        if len (blog_title) < 1:
            title_error = 'Must have content!'

        if not body_error and not title_error:
        
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            url = '/blog?id=' + str(new_blog.id)
            return redirect(url)

        else:
            return render_template('newpost.html',body_error=body_error,title_error=title_error)

    else:

        return render_template('newpost.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog(): 

    if request.args:
        blog_id = request.args.get("id")
        blog = Blog.query.get(blog_id)
        return render_template('single_post.html',blog=blog)


    else:
        blog_list = Blog.query.all()

        return render_template('blog.html',blog_list=blog_list)

    #@app.route('/single_post')
    #def view():

    #return redirect('/blog?id={blog.id}')

    #else:
          
            
           # single_post = request.args.get['id']
            #single_blog = Blog.query.filter_by().first()

        #return render_template('/single_post.html')
            
      #      single_post = Blog.query.filter_by().first()
        #single_post = request.args.get('id')
       # return render_template('single_post.html', single_post=single_post, title="Post")
        



if __name__ == '__main__':

    app.run()
 
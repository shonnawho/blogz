from flask import Flask, redirect, render_template, request
import os
import jinja2
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
#app.config['SQLALCHEMY_ECHO'] = True

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)



#db = SQLAlchemy(app)


#class for database
#class Blog(db.Model):

    #id = db.Column(db.Integer,primary_key=True)
    #title = db.Cloumn(db.String(200))
    #body = db.Cloumn(db.String(500))

    #def __init__(self,post)
    #self.post = post


    #Main route



@app.route('/', methods=['POST','GET'])
def index():

    blog_body= ''
    blog_title = ''

    if request.method == 'POST':
        post = request.form['blog_title','blog_body']
        
    return render_template('newpost.html',title="Build-a-Blog", blog_body="blog_body",blog_title="blog_title")



    #else:
        
        #return redirect('/blog?posts{0}'.format(posts))








#@app.route('/blog', methods=['POST', 'GET'])
#def blog():
    #post = request.args.get('posts')
    
    #return render_template ('blog.html', posts=posts)




    #if __name__ == '__main__':
app.run()
 
from flask import Flask, redirect, render_template, request, flash, session
import os
import jinja2
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 's1i9r8p6'





#class for database
class Blog(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __init__(self,title,body,owner_id):
        self.title = title
        self.body = body
        self.owner_id = owner_id


#db = SQLAlchemy(app)

#User class

class User(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(60))
    password = db.Column(db.String(60))
    blogs = db.relationship('Blog',backref='user')


    def __init__(self,username, password):
        self.username = username
        self.password = password
        

#app.route('/')
#def index():

    #return redirect('/blog')


@app.route('/newpost', methods=['POST','GET'])
def newpost():


    if request.method == 'POST':
        
        blog_body = request.form['blog_body']
        blog_title = request.form['blog_title']
        username = request.form['username']


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


#signup handler
@app.route('/signup', methods= ['POST','GET'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_verify = request.form['password_verify']
        user = User.query.filter_by(username=username).first()

        username_error=''
        password_error=''
        password_verify_error=''

        #Adds a new user to the database
        if not user and len(password) > 3 and password == password_verify:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username            
            return redirect('/newpost')
        else:


            #leave username,password field empty
            if username == '' or password == '' or verify_pw == '':
                username_error ='please enter valid username'
                password_error = 'Please enter valid password'
                password_verify_error = "please enter valid password"


                #if username already exist
            existing_user = User.query.filter_by(username=username).first()
                
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                return redirect ('/newpost')


            else:
                return "<h1>Duplicate user</h1>"



                        
                
            





@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        password_error = ''
        username_error = ''


        if user and user.password == password: #checks if the user exist and with the match passwords
            session['username'] = username
            return redirect('/newpost')

            
            
        if username and not user.password == password:
            session['username'] = username
            return redirect('/login')
            

        if not username and not password:
            
            return redirect('/signup')
            
    else:
        
        return render_template('login.html')

                
                
        





#@app.route()
#def index():

#handles a POST and redirects to /blog after the user deletes the user name
#@app.route()
#def logout():
    






if __name__ == '__main__':

    app.run()
 
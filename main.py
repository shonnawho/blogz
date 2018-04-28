from flask import Flask, redirect, render_template, request, session
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

    def __init__(self,title,body,owner):
        self.title = title
        self.body = body
        self.owner = owner




#User class

class User(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(60))
    password = db.Column(db.String(60))
    blogs = db.relationship('Blog',backref='owner')


    def __init__(self,username, password):
        self.username = username
        self.password = password
        
@app.before_request
def require_login():
    allowed_routes = ['login','blog','index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect ('/login')



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        password_error = ''
        username_error = ''
        
        if (not user):
            username_error = "that username doesn't exist"
            return render_template('login.html', username_error=username_error)

        if user and user.password == password: #checks if the user exist and with the match passwords
            session['username'] = username
            return redirect('/newpost')

            
            
        if user and not user.password == password:
            session['username'] = username
            password_error = " Password do not match our records"
            return render_template('/login.html',password_error=password_error)
            

        if not username and not user.password == password:
            return redirect('/signup')
            
    else:
        
        return render_template('login.html')


@app.route('/newpost', methods=['POST','GET'])
def newpost():

    if request.method == 'GET':
    
        return render_template('newpost.html', title="Add a Blog Entry")

    if request.method == 'POST':

            
        blog_body = request.form['blog_body']
        blog_title = request.form['blog_title']
        owner= User.query.filter_by(username=session['username']).first()


        title_error = ''
        body_error = ''


        if len (blog_body) < 1:
            body_error = 'Must have content!'


        if len (blog_title) < 1:
            title_error = 'Must have content!'

        if not body_error and not title_error:
            #owner_id = User.query.filter_by().first()
            new_blog = Blog(blog_title, blog_body, owner)
            db.session.add(new_blog)
            db.session.commit()
            url = '/blog?id=' + str(new_blog.id)           
            return redirect(url)
            
        else:
            return render_template('/newpost.html', owner=owner, body_error=body_error,title_error=title_error)

    else:

        return render_template('/newpost.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog(): 

    #if request.method = 'GET':


    if request.args.get("id"):
        blog_id = request.args.get("id")
        blog_list = Blog.query.filter_by(id=blog_id).all()
        

    elif request.args.get("user"):

        
        owner_id = request.args.get("user")
        blog_list = Blog.query.filter_by(owner_id=owner_id).all()

    
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

        existing_user = User.query.filter_by(username=username).first()
        
        if (existing_user):
            username_error = 'that username is already being used'
            return render_template('signup.html', username_error=username_error)

        #Adds a new user to the database
        if len(password) > 3 and password == password_verify:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username            
            return redirect('/newpost')
        
        else:
            
            
            if username == '' or len(username) < 3:
                username_error ='Not a valid username.  Usernames should be at least 3 chars.'

            if password == '' or password_verify == '' or len(password) < 3:
                password_error = 'Please enter valid password'
                password_verify_error = "please enter valid password"

                return render_template('signup.html',username_error=username_error,
                            password_error=password_error,password_verify_error=password_verify_error)        

                    
            if existing_user:
                username_error = 'Username already exist!'

            if password != password_verify:
                
                password_verify_error = 'Passwords do not match!'
                return render_template('/signup.html',password_verify_error=password_verify_error)
            
            else:
                
                if not password_verify_error and not username_error:
                    
                    return redirect('/newpost')
    else:
        
        return render_template("/signup.html")


        


@app.route('/singleUser', methods=['GET'])
def singleUser():
    users = User.query.filter_by(username=session['owner_id']).first()
    user_id = request.args.get('users')
    blogs = blog.query.filter_by(username=user_id).all()
    return render_template('singleUser.html', users=users, blogs=blogs)


@app.route('/singlepost', methods=['GET'])
def single_post():
    blog_id = request.args.get('id')
    blog_post = Blog.query.get(blog_id)
    owner_id = blog_post.owner_id
    user = User.query.all()
    return render_template('single_post.html', user_id=blog_id, blog=blog_post, owner=user, username=user)





@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

#handles a POST and redirects to /blog after the user deletes the user name
@app.route('/logout', methods = ['POST','GET'])
def logout():
    del session['username']
    return redirect('/login')

if __name__ == '__main__':

    app.run()
 
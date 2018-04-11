from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
#app.config['SQLALCHEMY_ECHO'] = True

#db = SQLAlchemy(app)


#class for database
#class Blog(db.Model):

    #id = db.Column(db.Integer,primary_key=True)
    #title = db.Cloumn(db.String(200))
    #body = db.Cloumn(db.String(500))

    #def __init__(self,post)
    #self.post = post


    #Main route
posts = []


@app.route('/', methods=['POST','GET'])
def index():

    if request.method == 'POST':
        post = request.form['post']
        posts.append(post)

    return render_template('newpost.html',title="Build-a-Blog", posts=posts)

#@app.route('/blog', methods=['POST', 'GET'])
#def


# new post template
#@app.route('/newpost', methods=['POST', 'GET'])
#def newpost_valid():

    #return render_template('newpost.html')

    #if __name__ == '__main__':
app.run()
 
from flask import Flask, request, redirect, session, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user2 = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blog = db.relationship('Blog', backref='owner')
    
    def __init__(self, user2, password):
        self.user2 = user2
        self.password = password
    

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(1024))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

@app.route('/', methods=['GET'])
def home():
    users = User.query.all()
    return render_template("index.html",  users=users)


@app.route('/newpost', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_name = request.form['blog']
        blog_title = request.form['title']
        owner = User.query.filter_by(user2=session['user']).first()
        if  not blog_name or not blog_title:
            flash('Fill in Body', 'body')
            
            flash('Provide Blog title', 'title')
            return render_template ('newpost.html')   

        new_blog = Blog(blog_title,blog_name,owner)
        db.session.add(new_blog)
        db.session.commit()
        blogID = str(new_blog.id)
        ownerID = str(new_blog.owner_id)
        return redirect("/blog?id="+blogID+'&'+ownerID)
        
    else:
        return render_template ('newpost.html')


@app.route('/blog', methods=['GET'])
def blog():
    blogs = Blog.query.all()
    blog_id = request.args.get('id')
    blog_auth = request.args.get('user')
    
    
    #users = User.query.filter_by(owner=owner).all()
    if blog_id:
        blog_post = Blog.query.filter(Blog.id == blog_id).first()
        return render_template('blog.html', blog = blog_post)
    if blog_auth:
        userName = User.query.filter(User.user2 == blog_auth).first()
        blogAuth = Blog.query.filter(Blog.owner_id == userName.id)
        return render_template('single.html', posts= blogAuth)
        

    else:
        return render_template("main.html",  posts=blogs)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        usersname = request.form['username']
        password = request.form['password']
        users = User.query.filter_by(user2=usersname)
        if users.count() == 1:
            user = users.first()
            if password == user.password:
                session['user'] = user.user2
                flash('welcome back, ' +user.user2)
                return redirect("/newpost")
            else:
                flash("That's not a valid password", 'valPass')
        else:
            flash("That's not a valid username", 'userName')
        return render_template('login.html') 

@app.route("/logout", methods=['GET'])
def logout():
    if session:
        del session['user2']
        return redirect("/blog")
    else:
        return redirect("/blog")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    space = " "
    usrName2=""
    vrfy2=""
    passWrd2=""
    isTrue="True"
    if request.method == 'POST':
        user3 = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        if space in user3 or (len(user3) < 3 or len(user3) > 20):
            flash("That's not a valid username", 'userName')
            usrName2=""
            isTrue="False"
        else:
            usrName2=user3
        
        if  space in password or (len(password) < 3 or len(password) > 20):
            flash("That's not a valid password", 'valPass')
            flash('passwords did not match', 'verify')
            passWrd2=""
            vrfy2=""
            isTrue="False"
        
        if password != verify:
            flash('passwords did not match', 'verify')
            passWrd2=""
            vrfy2=""
            isTrue="False"
        
        if isTrue=="False":
            return render_template('signup.html', usrName=usrName2, vrfy=vrfy2, passWrd=passWrd2)  
        
        else:
            user= User(user2=user3, password=password)
            db.session.add(user)
            db.session.commit()
            session['user'] = user.user2

            return redirect("/newpost")
    else: 
        return render_template('signup.html') 
        
    




endpoints_without_login = ['login', 'signup', 'blog', 'home', 'index']

@app.before_request
def require_login():
    if not ('user2' in session or request.endpoint in endpoints_without_login):
        return redirect("/login")

if __name__ == '__main__':
    app.run()

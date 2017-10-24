from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:Khr0no$1@localhost:8889/Blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'dgfdg5v65fj51g621g6'

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Bloggz', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Bloggz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(75))
    content = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, content, owner):
        self.title = title
        self.content = content
        self.owner = owner

@app.before_request
def require_login():
    not_allowed = ['add_page']
    if 'username' not in session and request.endpoint in not_allowed:
        return redirect('/login')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['username']
    return redirect('/')

@app.route('/ind_blog', methods=['GET'])
def blog():
    id = request.args['id']
    post = Bloggz.query.filter_by(id=id).first()
    return render_template('/ind_blog.html', post=post)

@app.route('/single_user', methods=['GET'])
def user_page():
    id = request.args['id']
    posts = (reversed(Bloggz.query.filter_by(id=id).all()))
    return render_template('singleUser.html', id=id, posts=posts)

@app.route('/blog_submit', methods=['POST', 'GET'])
def blog_submit():
    owner = Users.query.filter_by(username=session['username']).first()
    title = ''
    content = ''
    valid=True
    title_error=''
    content_error=''
    
    if request.method == 'POST':
        title = request.form['blog-title']
        content = request.form['blog-content']
        
        if title=='':
            title_error="""Don't you want to title your Blog post?"""
            valid=False
        if content=='':
            content_error="""Where is your blog post? I don't see it anywhere!"""
            valid=False
        if valid is False: 
            return render_template('addnew.html', title_error=title_error, content_error=content_error)
        
        blog = Bloggz(title, content, owner)
        db.session.add(blog)
        db.session.commit()
        curr_id = str(blog.id)
    return redirect('/ind_blog?id='+curr_id)

@app.route('/add_new', methods=['POST', 'GET'])
def add_page():
    return render_template('/addnew.html')

@app.route("/log_val", methods=['GET', 'POST'])
def login_validation():
    username = ''
    password = ''
    username_error=''
    password_error=''
    valid=True

    if request.method == 'POST':
        username = request.form['user-name']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect('/')
        else:    
            return '<h1>ERROR!!</h1>' 

@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('/login.html')

@app.route("/reg_val", methods=['GET', 'POST'])
def register_validation():
    username = ''
    password = ''
    password2 = ''
    valid=True
    username_error=''
    password_error=''
    password2_error=''
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        existing_user = Users.query.filter_by(username=username).first()
        if username=='':
            username_error='Select a username'
            valid=False
        if len(password) >20 or len(password) <3:
            password_error='Password must be between 3 and 20 characters'
            valid=False
        if password2!=password or password2=='':
            password2_error='Password does not match'
            valid=False
        if valid is False: 
            return render_template('signup.html', username_error=username_error, password_error=password_error, password2_error=password2_error)
        if not existing_user:
            signup = Users(username, password)
            db.session.add(signup)
            db.session.commit()
            session['username'] = username
        return redirect('/')

@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('/signup.html')

@app.route('/posts', methods=['POST', 'GET'])
def posts():
    posts = (reversed(Bloggz.query.all()))
    return render_template('blog.html', posts=posts)

@app.route('/', methods=['POST', 'GET'])
def index():
    users = Users.query.all()
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run()
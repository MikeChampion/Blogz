from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:P@ssw0rd@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Bloggz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(75))
    content = db.Column(db.String(500))

    def __init__(self, title, content):
        self.title = title
        self.content = content



@app.route('/blog_submit', methods=['POST', 'GET'])
def blog_submit():
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
        blog = Bloggz(title, content)
        db.session.add(blog)
        db.session.commit()
        curr_id = str(blog.id)
    return redirect('/ind_blog?id='+curr_id)

@app.route('/ind_blog', methods=['POST', 'GET'])
def blog():
    id = request.args['id']
    post = Bloggz.query.filter_by(id=id).first()
    return render_template('/ind_blog.html', post=post)

@app.route('/add_new', methods=['POST', 'GET'])
def add_page():
    return render_template('/addnew.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    posts = (reversed(Bloggz.query.all()))
    
    return render_template('blog.html', posts=posts)

if __name__ == '__main__':
    app.run()
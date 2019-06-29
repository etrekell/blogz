from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:apples88@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(300))
    post_body = db.Column(db.String(15000))

    def __init__(self, title, body):
        self.post_title = title
        self.post_body = body

@app.route('/   ', methods=['GET', 'POST'])
def index():

    posts = Blog.query.all()
    return render_template('blog.html', title="Build a Blog", posts=posts)

@app.route('/new-post', methods=['GET', 'POST'])
def new_post():

    post_body = ''
    post_title = ''
    error_title = ''
    error_blog = ''

    if request.method == 'POST':
        post_title = request.form['post_title']
        post_body = request.form['post_body']
        if post_title == '':
            error_title = 'You need a title!'
        elif post_body == '':
            error_blog = 'You need a post!'
        else:
            new = Blog(post_title, post_body)
            db.session.add(new)
            db.session.commit()

            return redirect('/single-post?id={0}'.format(new.id))

    return render_template('new-post.html', title="New Post", error_title=error_title,
                           error_blog=error_blog, post_title=post_title, post_body=post_body)

@app.route('/single-post', methods=['GET'])
def single_post():

    get_id = request.args.get('id')
    posts = db.session.query(
        Blog.post_title, Blog.post_body).filter_by(id=get_id)
    return render_template('single-post.html', title="Single Post", posts=posts)

if __name__ == '__main__':
    app.run()

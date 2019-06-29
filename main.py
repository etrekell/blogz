from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:apples88@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# class Task(db.Model):

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120))
#     completed = db.Column(db.Boolean)

#     def __init__(self, name):
#         self.name = name
#         self.completed = False

# @app.route('/', methods=['POST', 'GET'])
# def index():

#     if request.method == 'POST':
#         task_name = request.form['task']
#         new_task = Task(task_name)
#         db.session.add(new_task)
#         db.session.commit()

#     tasks = Task.query.filter_by(completed=False).all()
#     completed_tasks = Task.query.filter_by(completed=True).all()
#     return render_template('todos.html', title="Get It Done!",
#                            tasks=tasks, completed_tasks=completed_tasks)

# @app.route('/delete-task', methods=['POST'])
# def delete_task():

#     task_id = int(request.form['task-id'])
#     task = Task.query.get(task_id)
#     task.completed = True
#     db.session.add(task)
#     db.session.commit()

#     return redirect('/')


# if __name__ == '__main__':
#     app.run()


class Blog(db.Model):

    #specify the data fields colums in this class
    #every class persistent/stored in a database will have a ID that functions as Primary key
    #id associated with the task class will go in to the designated column configured to a integer, and repersent the Primary key
    id = db.Column(db.Integer, primary_key=True)
    #name field column string data type with a max length of 120
    post_title = db.Column(db.String(245))
    #set completed database column
    #boolean to indicate if task has been completed
    post_body = db.Column(db.String(12000))

    #set constructor
    def __init__(self, title, body):
        self.post_title = title
        self.post_body = body
    #classes have to be caps


@app.route('/blog', methods=['GET', 'POST'])
def index():

    posts = Blog.query.all()
    return render_template('blog.html', title="Build a Blog", posts=posts)


@app.route('/new-post', methods=['GET', 'POST'])
def new_post():

    post_body = ''
    post_title = ''
    error_title = ''
    error_blog = ''

    #obtain input data
    if request.method == 'POST':
        post_title = request.form['post_title']
        post_body = request.form['post_body']
        if post_title == '':
            error_title = 'You might need a Title!'
        elif post_body == '':
            error_blog = 'Your going to need to type some buttons!'
        else:
            #insert into database
            #commit database add
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
    #redirect back to post page
    return render_template('single-post.html', title="Single Post", posts=posts)


#allows importing objects,classes without running main.py
if __name__ == '__main__':
    app.run()

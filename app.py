from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(400), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    messname = db.Column(db.String(400), nullable = False)
    rating = db.Column(db.Float(), nullable = False)
    num_of_rating = db.Column(db.Integer(), nullable = False)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_messname = request.form['messname']
        task_rating = request.form['rating']
        task_num_of_rating = 1
        new_task = Todo(content=task_content, messname=task_messname, rating=task_rating, num_of_rating=task_num_of_rating)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue'
    else :
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        # task.content = request.form['content']
        # task.messname = request.form['messname']
        val = float(request.form['rating'])
        # task.rating = task.rating + float(val)
        task.num_of_rating = task.num_of_rating + 1
        task.rating = (task.rating * (task.num_of_rating - 1) + val)/task.num_of_rating
        task.rating = '%.1f'%task.rating
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "ISSUE"

    else :
         return render_template('update.html', task=task)

# @app.route('/search/<int:id>', methods=['GET','POST'])
# def search():
# SEARCH FUCTION HERE
if __name__ == "__main__":
    app.run(debug=True)
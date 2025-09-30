from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Use environment variable for DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Home page: show all students
@app.route('/')
def home():
    students = Student.query.all()
    return render_template('home.html', students=students)

# Add student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        student = Student(name=name, email=email, age=age)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_student.html')

if __name__ == '__main__':
    app.run(debug=True)

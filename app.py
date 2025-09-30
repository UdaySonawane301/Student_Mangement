from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration (Render PostgreSQL URL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hr_erp_db_8xas_user:21KI8UbPkKhjHzbRniqlegAlF37pU6JH@dpg-d3dug9umcj7s73cu4s10-a/hr_erp_db_8xas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# Home page - show all students
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
        new_student = Student(name=name, email=email, age=age)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_student.html')

# Edit student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.email = request.form['email']
        student.age = request.form['age']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit_student.html', student=student)

# Delete student
@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, login_required, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)
app.secret_key = 'kusumachandashwini'

# For unique user access
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/dbmsproj2'
db = SQLAlchemy(app)

# ---------------------------
# Existing Models
# ---------------------------
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

class Department(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(100))

class Attendence(db.Model):
    aid = db.Column(db.Integer, primary_key=True)
    rollno = db.Column(db.String(100))
    attendance = db.Column(db.Integer())

class Trig(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    rollno = db.Column(db.String(100))
    action = db.Column(db.String(100))
    timestamp = db.Column(db.String(100))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(1000))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rollno = db.Column(db.String(50))
    sname = db.Column(db.String(50))
    sem = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    branch = db.Column(db.String(50))
    email = db.Column(db.String(50))
    number = db.Column(db.String(12))
    address = db.Column(db.String(100))
    # Relationship for subject assignment
    subjects = db.relationship('StudentSubject', backref='student', cascade="all, delete-orphan")

# ---------------------------
# New Models for Subject Management
# ---------------------------
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    # Relationship to StudentSubject
    students = db.relationship('StudentSubject', backref='subject', cascade="all, delete-orphan")

class StudentSubject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    exam_score = db.Column(db.Float)  # Score can be stored as float

# ---------------------------
# Routes
# ---------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/studentdetails')
def studentdetails():
    query = Student.query.all()
    return render_template('studentdetails.html', query=query)

@app.route('/triggers')
def triggers():
    query = Trig.query.all()
    return render_template('triggers.html', query=query)

@app.route('/department', methods=['POST', 'GET'])
def department():
    if request.method == "POST":
        dept = request.form.get('dept')
        query = Department.query.filter_by(branch=dept).first()
        if query:
            flash("Department Already Exist", "warning")
            return redirect('/department')
        dep = Department(branch=dept)
        db.session.add(dep)
        db.session.commit()
        flash("Department Added", "success")
    return render_template('department.html')

@app.route('/addattendance', methods=['POST', 'GET'])
def addattendance():
    query = Student.query.all()
    if request.method == "POST":
        rollno = request.form.get('rollno')
        attend = request.form.get('attend')
        print(attend, rollno)
        atte = Attendence(rollno=rollno, attendance=attend)
        db.session.add(atte)
        db.session.commit()
        flash("Attendance added", "warning")
    return render_template('attendance.html', query=query)

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == "POST":
        rollno = request.form.get('roll')
        bio = Student.query.filter_by(rollno=rollno).first()
        attend = Attendence.query.filter_by(rollno=rollno).first()
        return render_template('search.html', bio=bio, attend=attend)
    return render_template('search.html')

@app.route("/delete/<string:id>", methods=['POST', 'GET'])
@login_required
def delete(id):
    post = Student.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    flash("Slot Deleted Successful", "danger")
    return redirect('/studentdetails')

@app.route("/edit/<string:id>", methods=['POST', 'GET'])
@login_required
def edit(id):
    if request.method == "POST":
        rollno = request.form.get('rollno')
        sname = request.form.get('sname')
        sem = request.form.get('sem')
        gender = request.form.get('gender')
        branch = request.form.get('branch')
        email = request.form.get('email')
        num = request.form.get('num')
        address = request.form.get('address')
        post = Student.query.filter_by(id=id).first()
        post.rollno = rollno
        post.sname = sname
        post.sem = sem
        post.gender = gender
        post.branch = branch
        post.email = email
        post.number = num
        post.address = address
        db.session.commit()
        flash("Slot is Updated", "success")
        return redirect('/studentdetails')
    dept = Department.query.all()
    posts = Student.query.filter_by(id=id).first()
    return render_template('edit.html', posts=posts, dept=dept)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist", "warning")
            return render_template('signup.html')
        newuser = User(username=username, email=email, password=password)
        db.session.add(newuser)
        db.session.commit()
        flash("Signup Success Please Login", "success")
        return render_template('login.html')
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            flash("Login Success", "primary")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials", "danger")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Successful", "warning")
    return redirect(url_for('login'))

@app.route('/addstudent', methods=['POST', 'GET'])
@login_required
def addstudent():
    dept = Department.query.all()
    if request.method == "POST":
        rollno = request.form.get('rollno')
        sname = request.form.get('sname')
        sem = request.form.get('sem')
        gender = request.form.get('gender')
        branch = request.form.get('branch')
        email = request.form.get('email')
        num = request.form.get('num')
        address = request.form.get('address')
        query = Student(rollno=rollno, sname=sname, sem=sem, gender=gender, branch=branch, email=email, number=num, address=address)
        db.session.add(query)
        db.session.commit()
        flash("Booking Confirmed", "info")
    return render_template('student.html', dept=dept)

@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'

# ---------------------------
# New Routes for Subject Management
# ---------------------------
@app.route('/addsubject', methods=['GET', 'POST'])
@login_required
def addsubject():
    if request.method == 'POST':
        subject_name = request.form.get('subject_name')
        existing = Subject.query.filter_by(name=subject_name).first()
        if existing:
            flash("Subject already exists", "warning")
            return redirect('/addsubject')
        new_subject = Subject(name=subject_name)
        db.session.add(new_subject)
        db.session.commit()
        flash("Subject added successfully", "success")
        return redirect('/addsubject')
    return render_template('add_subject.html')

@app.route('/assignsubject', methods=['GET', 'POST'])
@login_required
def assignsubject():
    students = Student.query.all()
    subjects = Subject.query.all()
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        subject_id = request.form.get('subject_id')
        exam_score = request.form.get('exam_score')
        assign = StudentSubject(student_id=student_id, subject_id=subject_id, exam_score=exam_score)
        db.session.add(assign)
        db.session.commit()
        flash("Subject assigned and exam score recorded", "success")
        return redirect('/assignsubject')
    return render_template('assign_subject.html', students=students, subjects=subjects)

@app.route('/updatescore', methods=['GET', 'POST'])
@login_required
def updatescore():
    if request.method == 'POST':
        record_id = request.form.get('record_id')
        new_score = request.form.get('new_score')
        record = StudentSubject.query.filter_by(id=record_id).first()
        if record:
            record.exam_score = new_score
            db.session.commit()
            flash("Exam score updated", "success")
        else:
            flash("Record not found", "danger")
        return redirect('/updatescore')
    records = StudentSubject.query.all()
    return render_template('update_score.html', records=records)

@app.route('/report')
@login_required
def report():
    students = Student.query.all()
    rank_list = []
    for stu in students:
        total = 0
        count = 0
        for ss in stu.subjects:
            if ss.exam_score is not None:
                total += ss.exam_score
                count += 1
        avg_score = total / count if count > 0 else 0
        rank_list.append((stu, avg_score))
    rank_list.sort(key=lambda x: x[1], reverse=True)
    return render_template('report.html', rank_list=rank_list)

# Run the app
app.run(debug=True)
  
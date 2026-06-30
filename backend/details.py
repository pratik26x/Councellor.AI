from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the database model for student details
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    current_address = db.Column(db.String(255), nullable=False)
    permanent_address = db.Column(db.String(255))
    hobbies = db.Column(db.String(255))
    clubs = db.Column(db.String(255))
    volunteer_work = db.Column(db.String(255))
    languages_known = db.Column(db.String(255))
    platforms = db.Column(db.String(255))
    specializations = db.Column(db.String(255))
    certifications = db.Column(db.String(255))
    career_goals = db.Column(db.String(255))
    preferred_industries = db.Column(db.String(255))
    internships = db.Column(db.String(255))

    def __repr__(self):
        return f'<Student {self.full_name}>'

# Home route (render the form)
@app.route('/')
def home():
    return render_template('index.html')

# Submit form data to the database
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get form data
        full_name = request.form['full_name']
        dob = request.form['dob']
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        current_address = request.form['current_address']
        permanent_address = request.form['permanent_address']
        hobbies = request.form['hobbies']
        clubs = request.form['clubs']
        volunteer_work = request.form['volunteer_work']
        languages_known = request.form['languages_known']
        platforms = request.form['platforms']
        specializations = request.form['specializations']
        certifications = request.form['certifications']
        career_goals = request.form['career_goals']
        preferred_industries = request.form['preferred_industries']
        internships = request.form['internships']

        # Create a new student record
        new_student = Student(
            full_name=full_name, dob=dob, gender=gender, email=email, phone=phone,
            current_address=current_address, permanent_address=permanent_address,
            hobbies=hobbies, clubs=clubs, volunteer_work=volunteer_work,
            languages_known=languages_known, platforms=platforms, specializations=specializations,
            certifications=certifications, career_goals=career_goals, preferred_industries=preferred_industries,
            internships=internships
        )

        # Add the new student to the database
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('home'))  # Redirect to home after form submission

if __name__ == '__main__':
    db.create_all()  # Create the database tables
    app.run(debug=True)

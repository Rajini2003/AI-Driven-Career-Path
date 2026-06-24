from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/aidriven'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'

db = SQLAlchemy(app)

# CompanyDetails Model
class CompanyDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-generated ID
    CompanyName = db.Column(db.String(255), nullable=False)
    Address = db.Column(db.String(255), nullable=False)
    EmailID = db.Column(db.String(255), unique=True, nullable=False)
    Website = db.Column(db.String(255), nullable=False)
    ContactNumber = db.Column(db.String(15), nullable=False)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(50), nullable=False)


# CandidateDetails Model
class CandidateDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-generated ID
    FirstName = db.Column(db.String(50), nullable=False)
    MiddleName = db.Column(db.String(50))
    LastName = db.Column(db.String(50), nullable=False)
    Gender = db.Column(db.String(10), nullable=False)
    MobileNumber = db.Column(db.String(15), nullable=False)
    EmailID = db.Column(db.String(100), unique=True, nullable=False)
    TenthPercentage = db.Column(db.Float, nullable=False)
    TwelfthPercentage = db.Column(db.Float, nullable=False)
    Branch = db.Column(db.String(50), nullable=False)
    USNNumber = db.Column(db.String(20), unique=True, nullable=False)
    Password = db.Column(db.String(50), nullable=False)
    skills = db.Column(db.String(100), nullable=False)
    

# Define the admin model
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255), nullable=False)
    Password = db.Column(db.String(255), nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def _repr_(self):
        return f'<Contact {self.email}>'
    

class Jobs(db.Model):
    job_id = db.Column(db.Integer, primary_key=True, nullable=False)  # Primary key is defined here
    job_name = db.Column(db.String(100), nullable=False)
    job_location = db.Column(db.String(100), nullable=False)
    number_of_posts = db.Column(db.Integer, nullable=False)
    branch = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Job {self.job_name} - {self.job_location}>"
    

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    branch = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)

class ApplyDetails(db.Model):
    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    usn_number = db.Column(db.String(20), nullable=False)
    email_id = db.Column(db.String(100), nullable=False)
    mob = db.Column(db.String(15), nullable=False)

job_skills = {
    "Software Engineer": ["Python", "Java", "C++", "Algorithms", "Software Development"],
    "Data Analyst": ["SQL", "Data Visualization", "Excel", "Statistical Analysis"],
    "Accountant": ["Accounting Principles", "Tax Knowledge", "Budget Management", "Spreadsheet Proficiency"],
    "Financial Analyst": ["Accounting", "Data Analysis", "Excel Proficiency", "Communication Skill"],
    "Assistant Audit Officer": ["Financial Analysis", "Financial Analysis", "Legal Compliance", "Accounting Knowledge"],
    "Mobile App Developer": ["Programming Language(Kotlin,Java)", "UI/UX Design", "Testing and Debugging", "Framework Knowledge"],
    "Event Manager": ["Event Manager", "Budget Management", "Public Speaking", "Design Thinking","Creativity"]
    }


@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/placed_students')
def placed_students():
    return render_template('placed_students.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin_page')
def admin_page():
    return render_template('admin_page.html')

@app.route('/company_page')
def company_page():
    return render_template('company_page.html')

@app.route('/candidate_page')
def candidate_page():
    return render_template('candidate_page.html')


@app.route('/admin_home')
def admin_home():
    return render_template('admin_home.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    bca_count = CandidateDetails.query.filter_by(Branch='BCA').count()
    bcom_count = CandidateDetails.query.filter_by(Branch='BCOM').count()
    ba_count = CandidateDetails.query.filter_by(Branch='BA').count()
    mcom_count = CandidateDetails.query.filter_by(Branch='MCOM').count()
    mca_count = CandidateDetails.query.filter_by(Branch='MCA').count()
    company_count = CompanyDetails.query.count()
    job_count = Jobs.query.count()
    applications_count = ApplyDetails.query.count()  # Add this line
    
    return render_template('admin_dashboard.html', 
                         bca_count=bca_count, 
                         bcom_count=bcom_count, 
                         ba_count=ba_count, 
                         mcom_count=mcom_count, 
                         mca_count=mca_count, 
                         company_count=company_count,
                         job_count=job_count,
                         applications_count=applications_count)  # Add this parameter

@app.route('/admin_companies')
def admin_companies():
    companies = CompanyDetails.query.all()
    return render_template('admin_companies.html', companies=companies)

@app.route('/admin_candidate')
def admin_candidate():
    candidates = CandidateDetails.query.all()
    return render_template('admin_candidate.html', candidates=candidates)

@app.route('/admin_search_by_branch', methods=['GET', 'POST'])
def admin_search_by_branch():
    candidates = []
    if request.method == 'POST':
        branch = request.form['branch']
        candidates = CandidateDetails.query.filter_by(Branch=branch).all()
    return render_template('admin_search_by_branch.html', candidates=candidates)

@app.route('/admin_notifications', methods=['GET', 'POST'])
def admin_notifications():
    if request.method == 'POST':
        branch = request.form['branch']
        message = request.form['message']

        # Save the notification to the database
        new_notification = Notification(branch=branch, message=message)
        db.session.add(new_notification)
        db.session.commit()

        # Get the email addresses of candidates in the selected branch
        candidates = CandidateDetails.query.filter_by(Branch=branch).all()
        email_addresses = [candidate.EmailID for candidate in candidates]

        # Email configuration
        sender_email = "3rdyear112233@gmail.com"  # Replace with your email
        password = "gggw wyfl uxsz jzpy"  # Replace with your app-specific password

        # Create the email
        subject = "Notification"
        body = f"""
        Hello,

        {message}

        Best regards,
        Admin
        """

        # Create a MIMEText object
        email_message = MIMEMultipart()
        email_message["From"] = sender_email
        email_message["Subject"] = subject
        email_message.attach(MIMEText(body, "plain"))

        # Send the email to each candidate
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                for email in email_addresses:
                    email_message["To"] = email
                    server.sendmail(sender_email, email, email_message.as_string())
            flash('Notification sent successfully!', 'success')
        except smtplib.SMTPAuthenticationError:
            flash('Error: Authentication failed. Check your email and password.', 'danger')
        except Exception as e:
            flash(f'Error: {e}', 'danger')

    return render_template('admin_notifications.html')

@app.route('/company_home')
def company_home():
    return render_template('company_home.html')

@app.route('/company_dashboard')
def company_dashboard():
    bca_count = CandidateDetails.query.filter_by(Branch='BCA').count()
    bcom_count = CandidateDetails.query.filter_by(Branch='BCOM').count()
    ba_count = CandidateDetails.query.filter_by(Branch='BA').count()
    mcom_count = CandidateDetails.query.filter_by(Branch='MCOM').count()
    mca_count = CandidateDetails.query.filter_by(Branch='MCA').count()
    return render_template('company_dashboard.html', bcacount=bca_count, bcom_count=bcom_count, ba_count=ba_count, mcom_count=mcom_count,mca_count=mca_count)

@app.route('/company_add_or_delete_jobs', methods=['GET', 'POST'])
def company_add_or_delete_jobs():
    if request.method == 'POST':
        job_id = request.form['job_id']
        job_name = request.form['job_name']
        job_location = request.form['job_location']
        number_of_posts = request.form['number_of_posts']
        branch = request.form['branch']

        try:
            # Create a new job entry
            new_job = Jobs(
            job_id = job_id,
            job_name=job_name,
            job_location=job_location,
            number_of_posts=number_of_posts,
            branch=branch
            )
            
            db.session.add(new_job)
            db.session.commit()

            flash('Job added successfully!', 'success')
            return redirect(url_for('company_add_or_delete_jobs'))
        except OperationalError:
            flash('Database connection error. Please try again later.', 'danger')
            return redirect(url_for('company_add_or_delete_jobs'))
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
            return redirect(url_for('company_add_or_delete_jobs'))

    return render_template('company_add_or_delete_jobs.html')

@app.route('/company_delete_jobs', methods=['GET', 'POST'])
def company_delete_jobs():
    if request.method == 'POST':
        job_id = request.form['job_id']
        job = Jobs.query.get(job_id)
        if job:
            db.session.delete(job)
            db.session.commit()
            flash('Job deleted successfully!', 'success')
        else:
            flash('Job not found!', 'danger')
    jobs = Jobs.query.all()
    return render_template('company_delete_jobs.html', jobs=jobs)



@app.route('/company_candidates_search', methods=['GET', 'POST'])
def company_candidates_search():
    candidates = []
    if request.method == 'POST':
        branch = request.form['branch']
        candidates = CandidateDetails.query.filter_by(Branch=branch).all()
    return render_template('company_candidates_search.html', candidates=candidates)

@app.route('/candidate_home')
def candidate_home():
    return render_template('candidate_home.html')

@app.route('/candidate_dashboard')
def candidate_dashboard():
    bca_count = CandidateDetails.query.filter_by(Branch='BCA').count()
    bcom_count = CandidateDetails.query.filter_by(Branch='BCOM').count()
    ba_count = CandidateDetails.query.filter_by(Branch='BA').count()
    mcom_count = CandidateDetails.query.filter_by(Branch='MCOM').count()
    mca_count = CandidateDetails.query.filter_by(Branch='MCA').count()
    job_count = Jobs.query.count()
    company_count = CompanyDetails.query.count()
         
    branch = session['branch']
    USNNumber = session['username']
    EmailID = session['emailid']
    MobileNumber = session['mobilenumber']
    FirstName = session['firstname']
    skills = session['skills']
    
    # Get count of jobs applied by current user
    applied_jobs_count = ApplyDetails.query.filter_by(usn_number=USNNumber).count()
    
    return render_template('candidate_dashboard.html', 
                         bca_count=bca_count, 
                         bcom_count=bcom_count, 
                         ba_count=ba_count, 
                         mcom_count=mcom_count,
                         mca_count=mca_count, 
                         job_count=job_count, 
                         company_count=company_count,
                         branch=branch,
                         FirstName=FirstName,
                         USNNumber=USNNumber,
                         EmailID=EmailID,
                         MobileNumber=MobileNumber,
                         skills=skills,
                         applied_jobs_count=applied_jobs_count)  # Add this line

@app.route('/candidate_search_and_apply', methods=['GET', 'POST'])
def candidate_search_and_apply():
    jobs = Jobs.query.all()
    # Get current user's USN number from session
    usn_number = session.get('username')
    
    # Get all applications for this candidate
    applied_jobs = ApplyDetails.query.filter_by(usn_number=usn_number).all()
    # Create a set of job IDs that the candidate has already applied to
    applied_job_ids = {str(app.job_id) for app in applied_jobs}
    
    return render_template('candidate_search_and_apply.html', 
                         jobs=jobs, 
                         applied_job_ids=applied_job_ids)



@app.route('/candidate_search_and_apply1')
def candidate_search_and_apply1():
    # Get job details from URL parameters
    job_id = request.args.get('job_id')
    job_name = request.args.get('job_name')
    job_branch = request.args.get('job_branch')
    
    # Get candidate details from session
    firstname = session.get('firstname')
    usn_number = session.get('username')
    email_id = session.get('emailid')
    mobile_number = session.get('mobilenumber')
    
    try:
        # Create new application entry
        new_application = ApplyDetails(
            job_id=job_id,
            job_name=job_name,
            branch=job_branch,
            name=firstname,
            usn_number=usn_number,
            email_id=email_id,
            mob=mobile_number
        )
        
        # Save to database
        db.session.add(new_application)
        db.session.commit()
        
        flash('Job application submitted successfully!', 'success')
    except Exception as e:
        flash(f'Error submitting application: {str(e)}', 'danger')
    
    # Redirect back to job search page
    return redirect(url_for('candidate_search_and_apply'))

@app.route('/candidate_chatbot', methods=['GET', 'POST'])
def candidate_chatbot():
    if request.method == 'POST':
        user_input = request.form['user_input']
        response = chatbot_response(user_input)
        return render_template('candidate_chatbot.html', user_input=user_input, response=response)
    return render_template('candidate_chatbot.html')

@app.route('/candidate_match_my_skill_test')
def candidate_match_my_skill_test():
    # Convert skills string to list
    skills_string = session.get('skills', '').strip()
    user_skills = [skill.strip() for skill in skills_string.split(',')]

    # Get job recommendations
    recommended_jobs = recommend_jobs(user_skills)

    # Return both the original skills string and the processed skills list
    return render_template('candidate_match_my_skill_test.html',
                         skills_string=skills_string,
                         user_skills=user_skills,
                         recommended_jobs=recommended_jobs,
                         job_skills=job_skills)

def recommend_jobs(user_skills):
    recommendations = []
    
    # Check each job and compare the skills
    for job, skills in job_skills.items():
        # Calculate the number of matching skills
        matching_skills = set(user_skills) & set(skills)
        match_score = len(matching_skills)
        
        # If there is at least one matching skill, add the job to recommendations
        if match_score > 0:
            recommendations.append((job, match_score, matching_skills))
    
    # Sort recommendations by match score (in descending order)
    recommendations.sort(key=lambda x: x[1], reverse=True)
    
    return recommendations

@app.route('/candidate_job_apply_history')
def candidate_job_apply_history():
    # Get current user's USN number from session
    usn_number = session.get('username')
    
    # Get all applications for this candidate
    applied_jobs = ApplyDetails.query.filter_by(usn_number=usn_number).all()
    
    return render_template('candidate_job_apply_history.html', applications=applied_jobs)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return render_template('login.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        message = request.form['message']

        # Create new Contact object
        new_contact = Contact(email=email, message=message)

        # Add contact to database
        db.session.add(new_contact)
        db.session.commit()

        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/forgot_password_candidate', methods=['GET', 'POST'])
def forgot_password_candidate():
    if request.method == 'POST':
        email = request.form['email']
        user = CandidateDetails.query.filter_by(EmailID=email).first()

        if user:
            new_password = generate_password()
            user.Password = new_password
            db.session.commit()

            # Email configuration
            sender_email = "3rdyear112233@gmail.com"  # Replace with your email
            receiver_email = email  # Use the user's email
            password = "gggw wyfl uxsz jzpy"  # Replace with your app-specific password

            # Create the email
            subject = "Your New Password"
            body = f"""
            Hello,

            Your new password is: {new_password}

            Best regards,
            Your Name
            """

            # Create a MIMEText object
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject

            # Attach the body to the email
            message.attach(MIMEText(body, "plain"))

            # Send the email
            try:
                # Connect to the SMTP server (for Gmail, use 'smtp.gmail.com' and port 587)
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    # Start TLS for security
                    server.starttls()

                    # Debugging: Print server responses
                    server.set_debuglevel(1)

                    # Login to the email account
                    server.login(sender_email, password)

                    # Send the email
                    server.sendmail(sender_email, receiver_email, message.as_string())

                print("Email sent successfully!")
            except smtplib.SMTPAuthenticationError:
                print("Error: Authentication failed. Check your email and password.")
            except Exception as e:
                print(f"Error: {e}")

            flash(f"Your new password has been sent to your email: {email}", 'info')
            return redirect(url_for('login'))
        else:
            flash('Email not found!', 'danger')
            
    return render_template('forgot_password_candidate.html')

@app.route('/forgot_password_company', methods=['GET', 'POST'])
def forgot_password_company():
    if request.method == 'POST':
        email = request.form['email']
        user = CompanyDetails.query.filter_by(EmailID=email).first()

        if user:
            new_password = generate_password()
            user.Password = new_password
            db.session.commit()

            # Email configuration
            sender_email = "3rdyear112233@gmail.com"  # Replace with your email
            receiver_email = email  # Use the user's email
            password = "gggw wyfl uxsz jzpy"  # Replace with your app-specific password

            # Create the email
            subject = "Your New Password"
            body = f"""
            Hello,

            Your new password is: {new_password}

            Best regards,
            Your Name
            """

            # Create a MIMEText object
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject

            # Attach the body to the email
            message.attach(MIMEText(body, "plain"))

            # Send the email
            try:
                # Connect to the SMTP server (for Gmail, use 'smtp.gmail.com' and port 587)
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    # Start TLS for security
                    server.starttls()

                    # Debugging: Print server responses
                    server.set_debuglevel(1)

                    # Login to the email account
                    server.login(sender_email, password)

                    # Send the email
                    server.sendmail(sender_email, receiver_email, message.as_string())

                print("Email sent successfully!")
            except smtplib.SMTPAuthenticationError:
                print("Error: Authentication failed. Check your email and password.")
            except Exception as e:
                print(f"Error: {e}")

            flash(f"Your new password has been sent to your email: {email}", 'info')
            return redirect(url_for('login'))
        else:
            flash('Email not found!', 'danger')
            
    return render_template('forgot_password_company.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form['user_type']
        username = request.form['username']
        password = request.form['password']

        if user_type == 'admin':
            user = Admin.query.filter_by(Username=username, Password=password).first()
            if user:
                session['username'] = user.Username
                return redirect(url_for('admin_home'))
        elif user_type == 'company':
            user = CompanyDetails.query.filter_by(Username=username, Password=password).first()
            if user:
                session['username'] = user.Username
                return redirect(url_for('company_home'))
        elif user_type == 'candidate':
            user = CandidateDetails.query.filter_by(USNNumber=username, Password=password).first()
            if user:
                session['username'] = user.USNNumber
                session['branch'] = user.Branch
                session['emailid'] = user.EmailID
                session['mobilenumber'] = user.MobileNumber
                session['firstname'] = user.FirstName
                session['skills'] = user.skills
                return redirect(url_for('candidate_home'))

        flash('Invalid username or password. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/company_registration', methods=['GET', 'POST'])
def company_registration():
    if request.method == 'POST':
        CompanyName = request.form['companyname']
        Address = request.form['address']
        EmailID = request.form['emailid']
        Website = request.form['website']
        ContactNumber = request.form['contactnumber']
        Username = request.form['username']
        Password = request.form['password']

        # Check if username or email already exists in the database
        existing_user = CompanyDetails.query.filter((CompanyDetails.Username == Username) | (CompanyDetails.EmailID == EmailID)).first()

        if existing_user:
            flash('Username or Email is already registered. Please choose a different one.', 'danger')
            return redirect(url_for('company_registration'))

        try:
            # Create a new company user
            new_user = CompanyDetails(
                CompanyName=CompanyName, 
                Address=Address, 
                EmailID=EmailID, 
                Website=Website, 
                ContactNumber=ContactNumber, 
                Username=Username, 
                Password=Password
            )
            
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except OperationalError:
            flash('Database connection error. Please try again later.', 'danger')
            return redirect(url_for('company_registration'))
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
            return redirect(url_for('company_registration'))

    return render_template('company_registration.html')


@app.route('/candidate_registration', methods=['GET', 'POST'])
def candidate_registration():
    if request.method == 'POST':
        FirstName = request.form['firstname']
        MiddleName = request.form['middlename']
        LastName = request.form['lastname']
        Gender = request.form['gender']
        MobileNumber = request.form['mobilenumber']
        EmailID = request.form['emailid']
        TenthPercentage = request.form['tenthpercentage']
        TwelfthPercentage = request.form['twelfthpercentage']
        Branch = request.form['branch']
        USNNumber = request.form['usnnumber']
        Password = request.form['password']
        Skills = request.form['Skills']

         # Check if username or email already exists in the database
        existing_user = CandidateDetails.query.filter((CandidateDetails.USNNumber == USNNumber) | (CandidateDetails.EmailID == EmailID)).first()

        if existing_user:
            flash('Username or Email is already registered. Please choose a different one.', 'danger')
            return redirect(url_for('candidate_registration'))

        try:
            # Create a new company user
            new_user = CandidateDetails(
                FirstName=FirstName,
                MiddleName=MiddleName,
                LastName=LastName,
                Gender=Gender,
                MobileNumber=MobileNumber,
                EmailID=EmailID,
                TenthPercentage=TenthPercentage,
                TwelfthPercentage=TwelfthPercentage,
                Branch=Branch,USNNumber=USNNumber,
                Password=Password,
                skills=Skills)
            
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except OperationalError:
            flash('Database connection error. Please try again later.', 'danger')
            return redirect(url_for('candidate_registration'))
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
            return redirect(url_for('candidate_registration'))

    return render_template('candidate_registration.html')


# A dictionary with simple question-response pairs
responses = {
    "hi": ["Hello!", "Hi there!", "Hey! How can I help you?"],
    "how are you": ["I'm doing great, thank you!", "I'm just a bot, but I'm good!", "I'm doing well, how about you?"],
    "bye": ["Goodbye!", "See you later!", "Have a great day!"],
    "How can I find a job": ["You can start by creating a strong resume and applying on platforms like LinkedIn, Naukri, or Indeed. Networking, attending job fairs, and reaching out to recruiters can also help."],
    "What is the best way to prepare for a job interview": ["Research the company, practice common interview questions, dress professionally, and be confident. Make sure to highlight your skills relevant to the role."],
    "What jobs can I get with a B.Com degree": [ "You could pursue roles like accountant, financial analyst, banker, tax consultant, or work in fields like marketing and management."],
}


def chatbot_response(user_input):
    # Convert the user input to lowercase for easier matching
    user_input = user_input.lower()

    # Check if the user input matches a known question
    for key in responses:
        if key in user_input:
            return random.choice(responses[key])
    
    # Default response if no match is found
    return "I'm sorry, I don't understand that."

if __name__ == '__main__':
    app.run(debug=True)

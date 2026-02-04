from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
app.config['DATABASE'] = 'job_portal.db'

# Database initialization
def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'employer', 'jobseeker')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Employers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            company_name TEXT NOT NULL,
            contact_person TEXT,
            phone TEXT,
            address TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Jobseekers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobseekers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT,
            address TEXT,
            skills TEXT,
            experience TEXT,
            education TEXT,
            resume_path TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employer_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            requirements TEXT,
            location TEXT,
            salary_range TEXT,
            job_type TEXT,
            status TEXT DEFAULT 'active' CHECK(status IN ('active', 'closed')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employer_id) REFERENCES employers(id) ON DELETE CASCADE
        )
    ''')
    
    # Applications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            jobseeker_id INTEGER NOT NULL,
            cover_letter TEXT,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'reviewed', 'shortlisted', 'rejected')),
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
            FOREIGN KEY (jobseeker_id) REFERENCES jobseekers(id) ON DELETE CASCADE,
            UNIQUE(job_id, jobseeker_id)
        )
    ''')
    
    # Create admin user if not exists
    cursor.execute("SELECT * FROM users WHERE email = 'admin@jobportal.com'")
    if not cursor.fetchone():
        admin_password = generate_password_hash('admin123')
        cursor.execute(
            "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
            ('admin@jobportal.com', admin_password, 'admin')
        )
    
    conn.commit()
    conn.close()

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# Decorators for authentication
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            if session.get('role') not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Routes
@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['role'] = user['role']
            
            flash(f'Welcome back!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@app.route('/register/<role>', methods=['GET', 'POST'])
def register(role):
    """User registration"""
    if role not in ['employer', 'jobseeker']:
        flash('Invalid registration type.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html', role=role)
        
        conn = get_db()
        
        # Check if email exists
        existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if existing_user:
            flash('Email already registered.', 'danger')
            conn.close()
            return render_template('register.html', role=role)
        
        # Create user
        hashed_password = generate_password_hash(password)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (email, password, role) VALUES (?, ?, ?)',
            (email, hashed_password, role)
        )
        user_id = cursor.lastrowid
        
        # Create role-specific profile
        if role == 'employer':
            company_name = request.form.get('company_name')
            contact_person = request.form.get('contact_person')
            phone = request.form.get('phone')
            address = request.form.get('address')
            
            cursor.execute(
                'INSERT INTO employers (user_id, company_name, contact_person, phone, address) VALUES (?, ?, ?, ?, ?)',
                (user_id, company_name, contact_person, phone, address)
            )
        
        elif role == 'jobseeker':
            full_name = request.form.get('full_name')
            phone = request.form.get('phone')
            address = request.form.get('address')
            
            cursor.execute(
                'INSERT INTO jobseekers (user_id, full_name, phone, address) VALUES (?, ?, ?, ?)',
                (user_id, full_name, phone, address)
            )
        
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', role=role)

@app.route('/dashboard')
@login_required
def dashboard():
    """Role-based dashboard"""
    role = session.get('role')
    
    if role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif role == 'employer':
        return redirect(url_for('employer_dashboard'))
    elif role == 'jobseeker':
        return redirect(url_for('jobseeker_dashboard'))
    
    return redirect(url_for('index'))

# Admin routes
@app.route('/admin/dashboard')
@role_required('admin')
def admin_dashboard():
    """Admin dashboard with statistics"""
    conn = get_db()
    
    # Get statistics
    stats = {
        'total_jobs': conn.execute('SELECT COUNT(*) as count FROM jobs').fetchone()['count'],
        'total_employers': conn.execute('SELECT COUNT(*) as count FROM employers').fetchone()['count'],
        'total_jobseekers': conn.execute('SELECT COUNT(*) as count FROM jobseekers').fetchone()['count'],
        'total_applications': conn.execute('SELECT COUNT(*) as count FROM applications').fetchone()['count']
    }
    
    # Daily stats (last 7 days)
    stats['daily_jobs'] = conn.execute(
        "SELECT COUNT(*) as count FROM jobs WHERE DATE(created_at) = DATE('now')"
    ).fetchone()['count']
    
    stats['weekly_jobs'] = conn.execute(
        "SELECT COUNT(*) as count FROM jobs WHERE created_at >= DATE('now', '-7 days')"
    ).fetchone()['count']
    
    stats['monthly_jobs'] = conn.execute(
        "SELECT COUNT(*) as count FROM jobs WHERE created_at >= DATE('now', '-30 days')"
    ).fetchone()['count']
    
    stats['yearly_jobs'] = conn.execute(
        "SELECT COUNT(*) as count FROM jobs WHERE created_at >= DATE('now', '-365 days')"
    ).fetchone()['count']
    
    conn.close()
    
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/jobs')
@role_required('admin')
def admin_jobs():
    """Admin view all jobs"""
    conn = get_db()
    jobs = conn.execute('''
        SELECT j.*, e.company_name 
        FROM jobs j
        JOIN employers e ON j.employer_id = e.id
        ORDER BY j.created_at DESC
    ''').fetchall()
    conn.close()
    
    return render_template('admin/jobs.html', jobs=jobs)

@app.route('/admin/employers')
@role_required('admin')
def admin_employers():
    """Admin view all employers"""
    conn = get_db()
    employers = conn.execute('''
        SELECT e.*, u.email, u.created_at 
        FROM employers e
        JOIN users u ON e.user_id = u.id
        ORDER BY u.created_at DESC
    ''').fetchall()
    conn.close()
    
    return render_template('admin/employers.html', employers=employers)

@app.route('/admin/jobseekers')
@role_required('admin')
def admin_jobseekers():
    """Admin view all jobseekers"""
    conn = get_db()
    jobseekers = conn.execute('''
        SELECT js.*, u.email, u.created_at 
        FROM jobseekers js
        JOIN users u ON js.user_id = u.id
        ORDER BY u.created_at DESC
    ''').fetchall()
    conn.close()
    
    return render_template('admin/jobseekers.html', jobseekers=jobseekers)

@app.route('/admin/delete/<entity>/<int:id>', methods=['POST'])
@role_required('admin')
def admin_delete(entity, id):
    """Admin delete entities"""
    conn = get_db()
    
    if entity == 'job':
        conn.execute('DELETE FROM jobs WHERE id = ?', (id,))
        flash('Job deleted successfully.', 'success')
    elif entity == 'employer':
        conn.execute('DELETE FROM users WHERE id = (SELECT user_id FROM employers WHERE id = ?)', (id,))
        flash('Employer deleted successfully.', 'success')
    elif entity == 'jobseeker':
        conn.execute('DELETE FROM users WHERE id = (SELECT user_id FROM jobseekers WHERE id = ?)', (id,))
        flash('Jobseeker deleted successfully.', 'success')
    
    conn.commit()
    conn.close()
    
    return redirect(request.referrer or url_for('admin_dashboard'))

# Employer routes
@app.route('/employer/dashboard')
@role_required('employer')
def employer_dashboard():
    """Employer dashboard"""
    conn = get_db()
    
    employer = conn.execute('''
        SELECT * FROM employers WHERE user_id = ?
    ''', (session['user_id'],)).fetchone()
    
    jobs = conn.execute('''
        SELECT j.*, COUNT(a.id) as application_count
        FROM jobs j
        LEFT JOIN applications a ON j.id = a.job_id
        WHERE j.employer_id = ?
        GROUP BY j.id
        ORDER BY j.created_at DESC
    ''', (employer['id'],)).fetchall()
    
    conn.close()
    
    return render_template('employer/dashboard.html', employer=employer, jobs=jobs)

@app.route('/employer/post-job', methods=['GET', 'POST'])
@role_required('employer')
def post_job():
    """Employer post new job"""
    if request.method == 'POST':
        conn = get_db()
        employer = conn.execute('SELECT * FROM employers WHERE user_id = ?', (session['user_id'],)).fetchone()
        
        title = request.form.get('title')
        description = request.form.get('description')
        requirements = request.form.get('requirements')
        location = request.form.get('location')
        salary_range = request.form.get('salary_range')
        job_type = request.form.get('job_type')
        
        conn.execute('''
            INSERT INTO jobs (employer_id, title, description, requirements, location, salary_range, job_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (employer['id'], title, description, requirements, location, salary_range, job_type))
        
        conn.commit()
        conn.close()
        
        flash('Job posted successfully!', 'success')
        return redirect(url_for('employer_dashboard'))
    
    return render_template('employer/post_job.html')

@app.route('/employer/job/<int:job_id>/applications')
@role_required('employer')
def view_applications(job_id):
    """Employer view applications for a job"""
    conn = get_db()
    
    # Verify job belongs to employer
    employer = conn.execute('SELECT * FROM employers WHERE user_id = ?', (session['user_id'],)).fetchone()
    job = conn.execute('SELECT * FROM jobs WHERE id = ? AND employer_id = ?', (job_id, employer['id'])).fetchone()
    
    if not job:
        flash('Job not found.', 'danger')
        conn.close()
        return redirect(url_for('employer_dashboard'))
    
    applications = conn.execute('''
        SELECT a.*, js.full_name, js.phone, u.email as jobseeker_email, js.skills, js.experience
        FROM applications a
        JOIN jobseekers js ON a.jobseeker_id = js.id
        JOIN users u ON js.user_id = u.id
        WHERE a.job_id = ?
        ORDER BY a.applied_at DESC
    ''', (job_id,)).fetchall()
    
    conn.close()
    
    return render_template('employer/applications.html', job=job, applications=applications)

# Jobseeker routes
@app.route('/jobseeker/dashboard')
@role_required('jobseeker')
def jobseeker_dashboard():
    """Jobseeker dashboard"""
    conn = get_db()
    
    jobseeker = conn.execute('''
        SELECT js.*, u.email
        FROM jobseekers js
        JOIN users u ON js.user_id = u.id
        WHERE js.user_id = ?
    ''', (session['user_id'],)).fetchone()
    
    # Get recent jobs
    jobs = conn.execute('''
        SELECT j.*, e.company_name
        FROM jobs j
        JOIN employers e ON j.employer_id = e.id
        WHERE j.status = 'active'
        ORDER BY j.created_at DESC
        LIMIT 10
    ''').fetchall()
    
    # Get applications
    applications = conn.execute('''
        SELECT a.*, j.title, e.company_name
        FROM applications a
        JOIN jobs j ON a.job_id = j.id
        JOIN employers e ON j.employer_id = e.id
        WHERE a.jobseeker_id = ?
        ORDER BY a.applied_at DESC
    ''', (jobseeker['id'],)).fetchall()
    
    conn.close()
    
    return render_template('jobseeker/dashboard.html', jobseeker=jobseeker, jobs=jobs, applications=applications)

@app.route('/jobseeker/jobs')
@role_required('jobseeker')
def browse_jobs():
    """Browse all available jobs"""
    conn = get_db()
    
    jobseeker = conn.execute('SELECT * FROM jobseekers WHERE user_id = ?', (session['user_id'],)).fetchone()
    
    jobs = conn.execute('''
        SELECT j.*, e.company_name,
               EXISTS(SELECT 1 FROM applications WHERE job_id = j.id AND jobseeker_id = ?) as already_applied
        FROM jobs j
        JOIN employers e ON j.employer_id = e.id
        WHERE j.status = 'active'
        ORDER BY j.created_at DESC
    ''', (jobseeker['id'],)).fetchall()
    
    conn.close()
    
    return render_template('jobseeker/jobs.html', jobs=jobs)

@app.route('/jobseeker/apply/<int:job_id>', methods=['GET', 'POST'])
@role_required('jobseeker')
def apply_job(job_id):
    """Apply for a job"""
    conn = get_db()
    
    jobseeker = conn.execute('SELECT * FROM jobseekers WHERE user_id = ?', (session['user_id'],)).fetchone()
    job = conn.execute('''
        SELECT j.*, e.company_name
        FROM jobs j
        JOIN employers e ON j.employer_id = e.id
        WHERE j.id = ? AND j.status = 'active'
    ''', (job_id,)).fetchone()
    
    if not job:
        flash('Job not found or no longer active.', 'danger')
        conn.close()
        return redirect(url_for('browse_jobs'))
    
    # Check if already applied
    existing = conn.execute(
        'SELECT * FROM applications WHERE job_id = ? AND jobseeker_id = ?',
        (job_id, jobseeker['id'])
    ).fetchone()
    
    if existing:
        flash('You have already applied for this job.', 'warning')
        conn.close()
        return redirect(url_for('browse_jobs'))
    
    if request.method == 'POST':
        cover_letter = request.form.get('cover_letter')
        
        conn.execute('''
            INSERT INTO applications (job_id, jobseeker_id, cover_letter)
            VALUES (?, ?, ?)
        ''', (job_id, jobseeker['id'], cover_letter))
        
        conn.commit()
        conn.close()
        
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('jobseeker_dashboard'))
    
    conn.close()
    return render_template('jobseeker/apply.html', job=job)

@app.route('/jobseeker/profile', methods=['GET', 'POST'])
@role_required('jobseeker')
def jobseeker_profile():
    """Jobseeker profile management"""
    conn = get_db()
    
    jobseeker = conn.execute('''
        SELECT js.*, u.email
        FROM jobseekers js
        JOIN users u ON js.user_id = u.id
        WHERE js.user_id = ?
    ''', (session['user_id'],)).fetchone()
    
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        skills = request.form.get('skills')
        experience = request.form.get('experience')
        education = request.form.get('education')
        
        conn.execute('''
            UPDATE jobseekers
            SET full_name = ?, phone = ?, address = ?, skills = ?, experience = ?, education = ?
            WHERE user_id = ?
        ''', (full_name, phone, address, skills, experience, education, session['user_id']))
        
        conn.commit()
        flash('Profile updated successfully!', 'success')
        
        jobseeker = conn.execute('''
            SELECT js.*, u.email
            FROM jobseekers js
            JOIN users u ON js.user_id = u.id
            WHERE js.user_id = ?
        ''', (session['user_id'],)).fetchone()
    
    conn.close()
    return render_template('jobseeker/profile.html', jobseeker=jobseeker)

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Initialize database on first run
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

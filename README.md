# Job Portal Web Application

A comprehensive, mobile-responsive job portal application built with Python Flask, SQLite, and Bootstrap. This application supports three user roles: Admin, Employer, and Jobseeker, each with their own set of features and access controls.

## Features

### 🎨 User Interface
- **Responsive Design**: Mobile-first design that works seamlessly across all devices
- **Sliding Sidebar Navigation**: Icon-only collapsed view that expands on hover
- **Modern Bootstrap UI**: Clean, professional interface with smooth animations
- **Role-based Dashboards**: Customized views for each user type

### 👥 User Roles

#### Admin
- View comprehensive dashboard with statistics (daily, weekly, monthly, yearly)
- Manage all jobs, employers, and jobseekers
- Delete any entity from the system
- Monitor platform activity

#### Employer
- Register with company information
- Post unlimited job listings
- View and manage job postings
- Review applications from jobseekers
- Track application counts per job

#### Jobseeker
- Register with personal profile
- Browse all active job listings
- Apply to jobs with cover letters
- Track application history and status
- Manage profile (skills, experience, education)

### 🔐 Security Features
- Password hashing with Werkzeug
- Session-based authentication
- Role-based access control
- CSRF protection
- SQL injection prevention

## Technology Stack

- **Backend**: Python 3.x, Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Bootstrap 5.3
- **Icons**: Bootstrap Icons
- **Authentication**: Flask Sessions, Werkzeug Security

## Project Structure

```
job_portal/
│
├── app.py                          # Main Flask application
├── job_portal.db                   # SQLite database (auto-created)
├── README.md                       # This file
│
└── templates/
    ├── base.html                   # Base template with layout
    ├── index.html                  # Landing page
    ├── login.html                  # Login page
    ├── register.html               # Registration page
    │
    ├── admin/
    │   ├── dashboard.html          # Admin dashboard
    │   ├── jobs.html               # Manage jobs
    │   ├── employers.html          # Manage employers
    │   └── jobseekers.html         # Manage jobseekers
    │
    ├── employer/
    │   ├── dashboard.html          # Employer dashboard
    │   ├── post_job.html           # Post new job
    │   └── applications.html       # View applications
    │
    └── jobseeker/
        ├── dashboard.html          # Jobseeker dashboard
        ├── jobs.html               # Browse jobs
        ├── apply.html              # Apply for job
        └── profile.html            # Manage profile
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd job-portal-application

# Or extract the ZIP file and navigate to the folder
cd job-portal-application
```

### Step 2: Install Dependencies
```bash
pip install flask werkzeug
```

Or create a requirements.txt file:
```txt
Flask==3.0.0
Werkzeug==3.0.0
```

Then install:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 4: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## Default Login Credentials

### Admin Account
- **Email**: admin@jobportal.com
- **Password**: admin123

**Important**: Change the admin password immediately in production!

## Usage Guide

### For Employers

1. **Register**: Click "Register as Employer" on the homepage
2. **Fill Details**: Provide company name, contact information
3. **Post Jobs**: After login, use "Post New Job" to create listings
4. **Review Applications**: Click on any job to view received applications

### For Jobseekers

1. **Register**: Click "Register as Job Seeker" on the homepage
2. **Complete Profile**: Update your profile with skills and experience
3. **Browse Jobs**: View all available job listings
4. **Apply**: Submit applications with optional cover letters
5. **Track**: Monitor your application status from the dashboard

### For Admins

1. **Login**: Use admin credentials
2. **Dashboard**: View comprehensive statistics
3. **Manage**: Access management pages for jobs, employers, and jobseekers
4. **Delete**: Remove any entity if needed

## Database Schema

### Users Table
- id (PRIMARY KEY)
- email (UNIQUE)
- password (HASHED)
- role (admin/employer/jobseeker)
- created_at

### Employers Table
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- company_name
- contact_person
- phone
- address

### Jobseekers Table
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- full_name
- phone
- address
- skills
- experience
- education
- resume_path

### Jobs Table
- id (PRIMARY KEY)
- employer_id (FOREIGN KEY)
- title
- description
- requirements
- location
- salary_range
- job_type
- status (active/closed)
- created_at

### Applications Table
- id (PRIMARY KEY)
- job_id (FOREIGN KEY)
- jobseeker_id (FOREIGN KEY)
- cover_letter
- status (pending/reviewed/shortlisted/rejected)
- applied_at

## Mobile Responsiveness

The application is fully responsive with:
- Collapsible sidebar on mobile (toggle with hamburger menu)
- Stacked layout for smaller screens
- Touch-friendly buttons and links
- Optimized forms for mobile input

## Customization

### Change Port
Edit `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)  # Change port here
```

### Change Secret Key
Edit `app.py`:
```python
app.secret_key = 'your-new-secret-key-here'
```

### Modify Colors
Edit styles in `templates/base.html`:
```css
:root {
    --primary-color: #667eea;  /* Change primary color */
}
```

## Production Deployment

### Important Changes for Production

1. **Disable Debug Mode**:
```python
app.run(debug=False)
```

2. **Change Secret Key**:
```python
app.secret_key = os.environ.get('SECRET_KEY') or 'strong-random-key'
```

3. **Use Production Database**:
Consider migrating to PostgreSQL or MySQL for better performance

4. **Enable HTTPS**:
Use a reverse proxy like Nginx with SSL certificates

5. **Environment Variables**:
Store sensitive data in environment variables

## Troubleshooting

### Database Issues
If you encounter database errors, delete `job_portal.db` and restart:
```bash
rm job_portal.db
python app.py
```

### Port Already in Use
Change the port in `app.py` or kill the process using the port:
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Import Errors
Ensure Flask is installed:
```bash
pip install --upgrade flask werkzeug
```

## Browser Compatibility

Tested and working on:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Future Enhancements

Potential features for future versions:
- Email notifications
- Resume upload functionality
- Advanced search and filters
- Application status updates
- Interview scheduling
- Messaging system between employers and jobseekers
- Analytics dashboard
- Export functionality (PDF reports)

## Support

For issues or questions:
- Create an issue in the repository
- Contact: support@jobportal.com

## License

This project is created for technical assessment purposes.

## Credits

Developed as part of a technical assessment demonstrating proficiency in:
- Python Flask framework
- SQLite database management
- Responsive web design with Bootstrap
- Role-based authentication and authorization
- Clean code architecture and best practices

---

**Note**: This is a demonstration project. For production use, additional security measures and optimizations are recommended.

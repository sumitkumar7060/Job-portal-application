# Quick Start Guide - Job Portal

## 🚀 Quick Setup (3 Steps)

### 1️⃣ Install Python
Make sure Python 3.7+ is installed:
```bash
python --version
# or
python3 --version
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application

**Linux/Mac:**
```bash
./run.sh
```

**Windows:**
```cmd
run.bat
```

**Or manually:**
```bash
python app.py
```

## 🌐 Access the Application

Open your browser and go to: **http://localhost:5000**

## 🔑 Demo Login Credentials

### Admin
- **Email**: admin@jobportal.com
- **Password**: admin123

### Test Accounts
You can register new employers and jobseekers directly from the application.

## 📱 Features

✅ Fully responsive (mobile, tablet, desktop)
✅ Role-based access (Admin, Employer, Jobseeker)
✅ Job posting and application management
✅ Profile management
✅ Real-time statistics dashboard
✅ Sliding sidebar navigation

## 🎯 What to Test

1. **As Admin:**
   - Login with admin credentials
   - View dashboard statistics
   - Manage jobs, employers, and jobseekers

2. **As Employer:**
   - Register a new employer account
   - Post a job listing
   - View applications

3. **As Jobseeker:**
   - Register a jobseeker account
   - Browse available jobs
   - Apply for jobs
   - Update profile

## 📂 Project Structure

```
job_portal/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # Full documentation
├── QUICKSTART.md      # This file
├── run.sh             # Linux/Mac launcher
├── run.bat            # Windows launcher
└── templates/         # HTML templates
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── admin/
    ├── employer/
    └── jobseeker/
```

## 🛠️ Troubleshooting

**Port already in use?**
Edit `app.py` and change the port:
```python
app.run(debug=True, port=8080)  # Change 5000 to 8080
```

**Database issues?**
Delete the database file and restart:
```bash
rm job_portal.db
python app.py
```

**Import errors?**
Reinstall dependencies:
```bash
pip install --upgrade flask werkzeug
```

## 📞 Support

For full documentation, see `README.md`

---

**Ready to go!** The application should now be running at http://localhost:5000 🎉

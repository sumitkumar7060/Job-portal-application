# Job Portal - System Architecture

## Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Browser                           │
│                  (HTML/CSS/Bootstrap/JS)                     │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ HTTP/HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask Application                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              URL Routing & Views                       │  │
│  │  • Landing Page        • Login/Logout                 │  │
│  │  • Registration        • Admin Routes                 │  │
│  │  • Employer Routes     • Jobseeker Routes             │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │           Authentication & Authorization              │  │
│  │  • Session Management  • Password Hashing             │  │
│  │  • Role-based Access   • Decorators                   │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Business Logic Layer                      │  │
│  │  • Job Management      • Application Processing       │  │
│  │  • User Management     • Profile Management           │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ SQL Queries
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  SQLite Database                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Users   │  │Employers │  │Jobseekers│  │   Jobs   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │             Applications                              │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## User Role Hierarchy

```
                    ┌──────────┐
                    │  Admin   │
                    │(Full     │
                    │Access)   │
                    └──────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                  │
   ┌────────┐                         ┌───────────┐
   │Employer│                         │ Jobseeker │
   │(Post & │                         │(Apply &   │
   │Manage) │                         │ Browse)   │
   └────────┘                         └───────────┘
```

## Database Schema

### Entity Relationship Diagram

```
┌─────────────┐
│   Users     │
│─────────────│
│ id (PK)     │─────┐
│ email       │     │
│ password    │     │
│ role        │     │
│ created_at  │     │
└─────────────┘     │
                    │
       ┌────────────┴─────────────┐
       │                          │
       │                          │
┌──────▼─────┐            ┌──────▼──────┐
│ Employers  │            │ Jobseekers  │
│────────────│            │─────────────│
│ id (PK)    │            │ id (PK)     │
│ user_id(FK)│            │ user_id(FK) │
│ company    │            │ full_name   │
│ contact    │            │ phone       │
│ phone      │            │ skills      │
│ address    │            │ experience  │
└────────────┘            │ education   │
      │                   └─────────────┘
      │                          │
      │                          │
┌─────▼────────┐                 │
│    Jobs      │                 │
│──────────────│                 │
│ id (PK)      │                 │
│ employer(FK) │                 │
│ title        │                 │
│ description  │                 │
│ requirements │                 │
│ location     │                 │
│ salary_range │                 │
│ job_type     │                 │
│ status       │                 │
│ created_at   │                 │
└──────────────┘                 │
       │                         │
       │    ┌────────────────────┘
       │    │
┌──────▼────▼────┐
│ Applications   │
│────────────────│
│ id (PK)        │
│ job_id (FK)    │
│ jobseeker(FK)  │
│ cover_letter   │
│ status         │
│ applied_at     │
└────────────────┘
```

## Application Flow

### User Registration & Authentication Flow

```
Start
  │
  ▼
Choose Role ────► Select: Employer or Jobseeker
  │
  ▼
Fill Registration Form
  │
  ├─► Email (unique check)
  ├─► Password (hashed)
  └─► Role-specific info
  │
  ▼
Create User Account
  │
  ├─► Insert into Users table
  └─► Insert into Employers/Jobseekers table
  │
  ▼
Redirect to Login
  │
  ▼
Enter Credentials
  │
  ▼
Verify ────► Check password hash
  │
  ▼
Create Session
  │
  └─► Store user_id, email, role
  │
  ▼
Redirect to Dashboard
```

### Job Application Flow

```
Jobseeker Dashboard
  │
  ▼
Browse Jobs ────► Filter by: type, location, etc.
  │
  ▼
Select Job ────► View details
  │
  ▼
Click "Apply"
  │
  ├─► Check if already applied
  │   └─► If yes: Show message
  │
  ▼
Fill Application Form
  │
  └─► Add cover letter (optional)
  │
  ▼
Submit Application
  │
  ├─► Insert into Applications table
  ├─► Set status: "pending"
  └─► Link: job_id + jobseeker_id
  │
  ▼
Confirmation ────► Redirect to dashboard
  │
  ▼
Track Status ────► View in "My Applications"
```

### Admin Management Flow

```
Admin Login
  │
  ▼
View Dashboard
  │
  ├─► Statistics (daily/weekly/monthly/yearly)
  ├─► Total jobs, employers, jobseekers
  └─► Applications count
  │
  ▼
Choose Management Section
  │
  ├─► Manage Jobs
  │   ├─► View all jobs
  │   └─► Delete jobs
  │
  ├─► Manage Employers
  │   ├─► View all employers
  │   └─► Delete employers (cascade delete)
  │
  └─► Manage Jobseekers
      ├─► View all jobseekers
      └─► Delete jobseekers (cascade delete)
```

## Security Measures

```
┌─────────────────────────────────────────┐
│         Security Layers                 │
├─────────────────────────────────────────┤
│ 1. Password Hashing (Werkzeug)         │
│    • SHA-256 + Salt                     │
│    • Pbkdf2:sha256                      │
├─────────────────────────────────────────┤
│ 2. Session Management                   │
│    • Secure session cookies             │
│    • Server-side session storage        │
├─────────────────────────────────────────┤
│ 3. Role-Based Access Control (RBAC)    │
│    • @login_required decorator          │
│    • @role_required decorator           │
├─────────────────────────────────────────┤
│ 4. SQL Injection Prevention             │
│    • Parameterized queries              │
│    • SQLite prepared statements         │
├─────────────────────────────────────────┤
│ 5. Input Validation                     │
│    • HTML5 form validation              │
│    • Server-side validation             │
├─────────────────────────────────────────┤
│ 6. Database Constraints                 │
│    • Foreign key constraints            │
│    • Unique constraints                 │
│    • Check constraints                  │
└─────────────────────────────────────────┘
```

## Responsive Design Strategy

```
┌────────────────────────────────────────────┐
│         Responsive Breakpoints              │
├────────────────────────────────────────────┤
│ Mobile First Approach                      │
│                                            │
│ • Base: Mobile (< 768px)                   │
│   └─► Stacked layout                       │
│   └─► Hamburger menu                       │
│   └─► Full-width cards                     │
│                                            │
│ • Tablet (768px - 992px)                   │
│   └─► 2-column grid                        │
│   └─► Expanded sidebar                     │
│   └─► Medium cards                         │
│                                            │
│ • Desktop (> 992px)                        │
│   └─► 3-4 column grid                      │
│   └─► Fixed sidebar                        │
│   └─► Optimized layout                     │
└────────────────────────────────────────────┘
```

## Technology Stack Details

```
Frontend
├── HTML5
│   └─► Semantic markup
├── CSS3
│   ├─► Flexbox layout
│   ├─► Grid system
│   └─► Animations
├── Bootstrap 5.3
│   ├─► Grid system
│   ├─► Components
│   └─► Utilities
└── JavaScript
    ├─► Sidebar toggle
    ├─► Form validation
    └─► Modal interactions

Backend
├── Python 3.x
├── Flask Framework
│   ├─► Routing
│   ├─► Templating (Jinja2)
│   └─► Session management
└── Werkzeug
    └─► Password hashing

Database
└── SQLite3
    ├─► Lightweight
    ├─► File-based
    └─► SQL standard
```

## Deployment Options

```
Development
  └─► Flask development server
      • Built-in server
      • Debug mode enabled
      • localhost:5000

Production (Recommended)
  ├─► Option 1: Gunicorn + Nginx
  │   └─► WSGI server + reverse proxy
  │
  ├─► Option 2: uWSGI + Nginx
  │   └─► Application server + proxy
  │
  └─► Option 3: Docker Container
      └─► Containerized deployment
```

## Performance Considerations

```
┌─────────────────────────────────────────┐
│     Performance Optimizations           │
├─────────────────────────────────────────┤
│ • Database Indexing                     │
│   └─► Primary keys auto-indexed        │
│   └─► Foreign keys indexed              │
│                                         │
│ • Query Optimization                    │
│   └─► JOIN operations minimized        │
│   └─► SELECT only needed columns       │
│                                         │
│ • Session Caching                       │
│   └─► Server-side session storage      │
│                                         │
│ • Static Asset Caching                  │
│   └─► Browser caching for CSS/JS       │
│                                         │
│ • Lazy Loading                          │
│   └─► Pagination for large lists       │
└─────────────────────────────────────────┘
```

This architecture provides a scalable, secure, and maintainable solution for the job portal application.

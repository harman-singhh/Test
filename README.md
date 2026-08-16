# CodeCraft Academy — Programming & Tech-Skills Tutoring Hub

A complete, professional full-stack tutoring website built with **HTML5, CSS3, JavaScript, Python Flask, PyMySQL, and MySQL (phpMyAdmin)**.

CodeCraft Academy is a **niche tutoring platform focused exclusively on programming and tech skills** (web dev, Python, data science, mobile, AI/ML, DevOps). Unlike a generic tutoring site, the dashboard supports managing **courses, tutors, testimonials, session bookings, and contact messages** — five content types instead of just one.

---

## ✨ Features

- Modern, responsive, gradient-based UI with animations and hover effects
- Public pages: Home, About, Courses, Contact, Book a Session
- Admin authentication with hashed passwords + Flask sessions
- Protected dashboard with 5 stat cards and quick actions
- **Add Course** (with image upload, price, duration, syllabus/demo links)
- **Edit / Delete Course**
- **Add Tutor** (with photo upload, expertise, experience)
- **View / Delete Tutors**
- **Add Testimonial** (with star rating + photo upload)
- **Session Bookings** management (students book directly from the site; admin updates status: Pending → Confirmed → Completed/Cancelled)
- **Contact Messages** inbox (view/delete)
- Secure file uploads (png/jpg/jpeg only), parameterized SQL queries, session-protected routes
- Client-side + server-side form validation

---

## 🗂️ Project Structure

```
CodeCraftAcademy/
│  app.py
│  requirements.txt
│  database.sql
│  config.py
│  README.md
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── dashboard.css
│   │   └── login.css
│   ├── js/
│   │   ├── script.js
│   │   └── dashboard.js
│   └── images/           (uploaded course/tutor/testimonial images)
│
└── templates/
    ├── index.html
    ├── about.html
    ├── courses.html
    ├── contact.html
    ├── book_session.html
    ├── login.html
    ├── dashboard.html
    ├── add_course.html
    ├── edit_course.html
    ├── add_tutor.html
    ├── view_tutors.html
    ├── add_testimonial.html
    ├── view_bookings.html
    └── view_messages.html
```

---

## 🚀 Installation & Setup

### 1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
```

### 2. Install requirements
```bash
pip install -r requirements.txt
```

### 3. Create the database
1. Open **phpMyAdmin**.
2. Import `database.sql` (it creates the `codecraft_academy_db` database and all tables, and inserts a default admin).
3. If needed, update your MySQL host/user/password in `config.py` or via environment variables:
   - `MYSQL_HOST` (default `localhost`)
   - `MYSQL_USER` (default `root`)
   - `MYSQL_PASSWORD` (default empty)
   - `MYSQL_DB` (default `codecraft_academy_db`)
   - `MYSQL_PORT` (default `3306`)

### 4. Run the Flask app
```bash
python app.py
```

The site will be available at **http://127.0.0.1:5000**

---

## 🔑 Default Admin Login

```
Email:    admin@gmail.com
Password: admin123
```

> On first run, `app.py` automatically re-hashes and repairs the default admin's password so this login always works, even if the placeholder hash in `database.sql` wasn't regenerated manually.

---

## 🧭 Route Map

| Route | Method | Description |
|---|---|---|
| `/` | GET | Home page |
| `/about` | GET | About page + tutor list |
| `/courses` | GET | Public courses listing |
| `/contact` | GET | Contact form |
| `/api/contact` | POST | Save contact message |
| `/book` | GET | Public session booking form |
| `/api/book` | POST | Save session booking |
| `/login` | GET | Admin login page |
| `/api/login` | POST | Authenticate admin |
| `/logout` | GET | Destroy session |
| `/dashboard` | GET | Protected dashboard |
| `/add_course` | GET/POST | Add a new course |
| `/edit_course/<id>` | GET/POST | Edit a course |
| `/delete_course/<id>` | GET | Delete a course |
| `/add_tutor` | GET/POST | Add a tutor |
| `/view_tutors` | GET | List tutors |
| `/delete_tutor/<id>` | GET | Remove a tutor |
| `/add_testimonial` | GET/POST | Add a testimonial |
| `/view_bookings` | GET | List session bookings |
| `/update_booking/<id>` | POST | Update booking status |
| `/view_messages` | GET | List contact messages |
| `/delete_message/<id>` | GET | Delete a contact message |

---

## 🔒 Security Notes

- Passwords are hashed with `werkzeug.security.generate_password_hash` / verified with `check_password_hash`
- All SQL queries use parameterized statements (PyMySQL `%s` placeholders) to prevent SQL injection
- Dashboard routes are protected by a `login_required` decorator checking Flask session
- File uploads are restricted to `.png`, `.jpg`, `.jpeg` and sanitized with `secure_filename`

---

## 📄 License

Built for educational/demo purposes. Customize freely for your own tutoring business.

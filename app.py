import os
from functools import wraps
from datetime import datetime

import pymysql
import pymysql.cursors
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from config import Config

app = Flask(__name__)
app.config.from_object(Config)


# ---------------------------------------------------------
# Database helpers
# ---------------------------------------------------------
def get_db_connection():
    return pymysql.connect(
        host=app.config["MYSQL_HOST"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        db=app.config["MYSQL_DB"],
        port=app.config["MYSQL_PORT"],
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


def ensure_default_admin():
    """Make sure the default admin login works out of the box,
    even though the SQL file ships with a placeholder hash."""
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id, password FROM admins WHERE email=%s", ("admin@gmail.com",))
            row = cur.fetchone()
            if row and not check_password_hash(row["password"], "admin123"):
                new_hash = generate_password_hash("admin123")
                cur.execute("UPDATE admins SET password=%s WHERE id=%s", (new_hash, row["id"]))
        conn.close()
    except Exception as e:
        print("Warning: could not verify default admin ->", e)


def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_id"):
            flash("Please login to access the dashboard.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ---------------------------------------------------------
# Public routes
# ---------------------------------------------------------
@app.route("/")
def index():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) AS c FROM courses")
        total_courses = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) AS c FROM tutors")
        total_tutors = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) AS c FROM bookings")
        total_students = cur.fetchone()["c"]
        cur.execute("SELECT * FROM testimonials ORDER BY created_at DESC LIMIT 6")
        testimonials = cur.fetchall()
    conn.close()
    return render_template(
        "index.html",
        total_courses=total_courses,
        total_tutors=total_tutors,
        total_students=total_students,
        testimonials=testimonials
    )


@app.route("/about")
def about():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tutors ORDER BY created_at DESC")
        tutors = cur.fetchall()
    conn.close()
    return render_template("about.html", tutors=tutors)


@app.route("/courses")
def courses():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM courses ORDER BY created_at DESC")
        all_courses = cur.fetchall()
    conn.close()
    return render_template("courses.html", courses=all_courses)


@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")


@app.route("/api/contact", methods=["POST"])
def api_contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Please fill in all required fields.", "error")
        return redirect(url_for("contact"))

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO contact_messages (name, email, phone, subject, message) "
            "VALUES (%s, %s, %s, %s, %s)",
            (name, email, phone, subject, message)
        )
    conn.close()

    flash("Thank you! Your message has been received.", "success")
    return redirect(url_for("contact"))


@app.route("/book", methods=["GET"])
def book():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id, title FROM courses ORDER BY title")
        all_courses = cur.fetchall()
    conn.close()
    return render_template("book_session.html", courses=all_courses)


@app.route("/api/book", methods=["POST"])
def api_book():
    student_name = request.form.get("student_name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    course_id = request.form.get("course_id") or None
    preferred_date = request.form.get("preferred_date") or None
    preferred_time = request.form.get("preferred_time", "").strip()
    message = request.form.get("message", "").strip()

    if not student_name or not email:
        flash("Name and email are required.", "error")
        return redirect(url_for("book"))

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO bookings (student_name, email, phone, course_id, preferred_date, "
            "preferred_time, message) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (student_name, email, phone, course_id, preferred_date, preferred_time, message)
        )
    conn.close()

    flash("Your session request has been submitted! We'll email you shortly.", "success")
    return redirect(url_for("book"))


# ---------------------------------------------------------
# Auth routes
# ---------------------------------------------------------
@app.route("/login", methods=["GET"])
def login():
    if session.get("admin_id"):
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/api/login", methods=["POST"])
def api_login():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM admins WHERE email=%s", (email,))
        admin = cur.fetchone()
    conn.close()

    if admin and check_password_hash(admin["password"], password):
        session["admin_id"] = admin["id"]
        session["admin_name"] = admin["username"]
        return redirect(url_for("dashboard"))

    flash("Invalid Email or Password", "error")
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# ---------------------------------------------------------
# Dashboard routes (protected)
# ---------------------------------------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) AS c FROM courses")
        total_courses = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) AS c FROM contact_messages")
        total_messages = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) AS c FROM tutors")
        total_tutors = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) AS c FROM testimonials")
        total_testimonials = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) AS c FROM bookings")
        total_bookings = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) AS c FROM bookings WHERE status='Pending'")
        pending_bookings = cur.fetchone()["c"]
        cur.execute("SELECT * FROM courses ORDER BY created_at DESC LIMIT 10")
        recent_courses = cur.fetchall()
    conn.close()
    return render_template(
        "dashboard.html",
        total_courses=total_courses,
        total_messages=total_messages,
        total_tutors=total_tutors,
        total_testimonials=total_testimonials,
        total_bookings=total_bookings,
        pending_bookings=pending_bookings,
        recent_courses=recent_courses
    )


# ---- Courses CRUD ----
@app.route("/add_course", methods=["GET", "POST"])
@login_required
def add_course():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()
        duration = request.form.get("duration", "").strip()
        price = request.form.get("price") or 0
        syllabus_link = request.form.get("syllabus_link", "").strip()
        demo_link = request.form.get("demo_link", "").strip()

        if not title or not description or not category:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("add_course"))

        image_filename = None
        file = request.files.get("image")
        if file and file.filename:
            if allowed_file(file.filename):
                image_filename = secure_filename(
                    f"{int(datetime.now().timestamp())}_{file.filename}"
                )
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))
            else:
                flash("Invalid image type. Only png, jpg, jpeg allowed.", "error")
                return redirect(url_for("add_course"))

        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO courses (title, description, category, image, duration, "
                "price, syllabus_link, demo_link) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (title, description, category, image_filename, duration,
                 price, syllabus_link, demo_link)
            )
        conn.close()
        flash("Course added successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("add_course.html")


@app.route("/edit_course/<int:course_id>", methods=["GET", "POST"])
@login_required
def edit_course(course_id):
    conn = get_db_connection()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()
        duration = request.form.get("duration", "").strip()
        price = request.form.get("price") or 0
        syllabus_link = request.form.get("syllabus_link", "").strip()
        demo_link = request.form.get("demo_link", "").strip()

        with conn.cursor() as cur:
            file = request.files.get("image")
            if file and file.filename:
                if allowed_file(file.filename):
                    image_filename = secure_filename(
                        f"{int(datetime.now().timestamp())}_{file.filename}"
                    )
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))
                    cur.execute(
                        "UPDATE courses SET title=%s, description=%s, category=%s, image=%s, "
                        "duration=%s, price=%s, syllabus_link=%s, demo_link=%s WHERE id=%s",
                        (title, description, category, image_filename, duration,
                         price, syllabus_link, demo_link, course_id)
                    )
                else:
                    flash("Invalid image type. Only png, jpg, jpeg allowed.", "error")
                    return redirect(url_for("edit_course", course_id=course_id))
            else:
                cur.execute(
                    "UPDATE courses SET title=%s, description=%s, category=%s, "
                    "duration=%s, price=%s, syllabus_link=%s, demo_link=%s WHERE id=%s",
                    (title, description, category, duration,
                     price, syllabus_link, demo_link, course_id)
                )
        conn.close()
        flash("Course updated successfully!", "success")
        return redirect(url_for("dashboard"))

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM courses WHERE id=%s", (course_id,))
        course = cur.fetchone()
    conn.close()

    if not course:
        flash("Course not found.", "error")
        return redirect(url_for("dashboard"))

    return render_template("edit_course.html", course=course)


@app.route("/delete_course/<int:course_id>")
@login_required
def delete_course(course_id):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM courses WHERE id=%s", (course_id,))
    conn.close()
    flash("Course deleted.", "success")
    return redirect(url_for("dashboard"))


# ---- Tutors ----
@app.route("/add_tutor", methods=["GET", "POST"])
@login_required
def add_tutor():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        expertise = request.form.get("expertise", "").strip()
        bio = request.form.get("bio", "").strip()
        experience_years = request.form.get("experience_years") or 0
        email = request.form.get("email", "").strip()

        if not name or not expertise:
            flash("Name and expertise are required.", "error")
            return redirect(url_for("add_tutor"))

        photo_filename = None
        file = request.files.get("photo")
        if file and file.filename:
            if allowed_file(file.filename):
                photo_filename = secure_filename(
                    f"{int(datetime.now().timestamp())}_{file.filename}"
                )
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_filename))
            else:
                flash("Invalid image type. Only png, jpg, jpeg allowed.", "error")
                return redirect(url_for("add_tutor"))

        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tutors (name, expertise, bio, experience_years, email, photo) "
                "VALUES (%s,%s,%s,%s,%s,%s)",
                (name, expertise, bio, experience_years, email, photo_filename)
            )
        conn.close()
        flash("Tutor added successfully!", "success")
        return redirect(url_for("view_tutors"))

    return render_template("add_tutor.html")


@app.route("/view_tutors")
@login_required
def view_tutors():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tutors ORDER BY created_at DESC")
        tutors = cur.fetchall()
    conn.close()
    return render_template("view_tutors.html", tutors=tutors)


@app.route("/delete_tutor/<int:tutor_id>")
@login_required
def delete_tutor(tutor_id):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM tutors WHERE id=%s", (tutor_id,))
    conn.close()
    flash("Tutor removed.", "success")
    return redirect(url_for("view_tutors"))


# ---- Testimonials ----
@app.route("/add_testimonial", methods=["GET", "POST"])
@login_required
def add_testimonial():
    if request.method == "POST":
        student_name = request.form.get("student_name", "").strip()
        course_taken = request.form.get("course_taken", "").strip()
        message = request.form.get("message", "").strip()
        rating = request.form.get("rating") or 5

        if not student_name or not message:
            flash("Student name and message are required.", "error")
            return redirect(url_for("add_testimonial"))

        photo_filename = None
        file = request.files.get("photo")
        if file and file.filename:
            if allowed_file(file.filename):
                photo_filename = secure_filename(
                    f"{int(datetime.now().timestamp())}_{file.filename}"
                )
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_filename))
            else:
                flash("Invalid image type. Only png, jpg, jpeg allowed.", "error")
                return redirect(url_for("add_testimonial"))

        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO testimonials (student_name, course_taken, message, rating, photo) "
                "VALUES (%s,%s,%s,%s,%s)",
                (student_name, course_taken, message, rating, photo_filename)
            )
        conn.close()
        flash("Testimonial added successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("add_testimonial.html")


# ---- Bookings ----
@app.route("/view_bookings")
@login_required
def view_bookings():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT bookings.*, courses.title AS course_title FROM bookings "
            "LEFT JOIN courses ON bookings.course_id = courses.id "
            "ORDER BY bookings.created_at DESC"
        )
        bookings = cur.fetchall()
    conn.close()
    return render_template("view_bookings.html", bookings=bookings)


@app.route("/update_booking/<int:booking_id>", methods=["POST"])
@login_required
def update_booking(booking_id):
    status = request.form.get("status")
    valid_statuses = {"Pending", "Confirmed", "Completed", "Cancelled"}
    if status not in valid_statuses:
        flash("Invalid status.", "error")
        return redirect(url_for("view_bookings"))

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("UPDATE bookings SET status=%s WHERE id=%s", (status, booking_id))
    conn.close()
    flash("Booking status updated.", "success")
    return redirect(url_for("view_bookings"))


# ---- Contact messages ----
@app.route("/view_messages")
@login_required
def view_messages():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM contact_messages ORDER BY created_at DESC")
        messages = cur.fetchall()
    conn.close()
    return render_template("view_messages.html", messages=messages)


@app.route("/delete_message/<int:message_id>")
@login_required
def delete_message(message_id):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM contact_messages WHERE id=%s", (message_id,))
    conn.close()
    flash("Message deleted.", "success")
    return redirect(url_for("view_messages"))


# Ensure default admin works under Gunicorn/WSGI production server
try:
    ensure_default_admin()
except Exception as _e:
    print("Could not auto-verify default admin on startup:", _e)


if __name__ == "__main__":
    app.run(debug=True)

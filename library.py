from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL

from flask import *

from auth import (
    login_required,
    admin_required,
    member_required,
    protect_routes
)

app = Flask(__name__)

app.secret_key = "library_secret_key"

protect_routes(app)

#  MYSQL DIRECT CONFIG (NO config.py) 
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "smart_library1"

mysql = MySQL(app)

# DASHBOARD 
@app.route('/base')
@app.route('/dashboard')
@admin_required
def dashboard():

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM members")
    total_members = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM issued_books WHERE status='Issued'")
    issued_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books")
    available_books = cursor.fetchone()[0]

    cursor.close()

    return render_template("dashboard.html",
                           total_books=total_books,
                           total_members=total_members,
                           issued_books=issued_books,
                           available_books=available_books)




from ml.recommendation import recommend_books

@app.route('/')
def home():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            book_id,
            book_name,
            author,
            category,
            image
        FROM books
    """)

    books = cursor.fetchall()

    recommendations = []

    if len(books) > 0:

        first_book = books[0][1]

        recommendations = recommend_books(
        first_book
        )

    cursor.close()

    return render_template(
        'home.html',
        books=books,
        recommendations=recommendations
    )
app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():

    if request.method == 'POST':

        # Save settings code
        print("Settings Saved")

        # Database update yahan hoga

        return redirect(url_for('settings'))

    return render_template('settings.html')

# BOOKS 
@app.route('/books')
@login_required
def books():

    search = request.args.get("search", "").strip()

    cursor = mysql.connection.cursor()

    
    # Search Books

    if search:

        cursor.execute("""
            SELECT *
            FROM books
            WHERE
                book_name LIKE %s
                OR author LIKE %s
                OR category LIKE %s
                OR isbn LIKE %s
        """, (

            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"

        ))

    else:

        cursor.execute("SELECT * FROM books")

    data = cursor.fetchall()

    cursor.close()

    books = []

    for b in data:

        books.append({

            "id": b[0],

            "title": b[1],

            "author": b[2],

            "category": b[3],

            "quantity": b[4],

            "available_quantity": b[5],

            "image": b[9] if b[9] else "default_book.jpg"

        })

    return render_template(

        "books.html",

        books=books,

        search=search

    )

@app.route('/add_books', methods=['GET', 'POST'])
@admin_required
def add_book():

    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO books(title,author,category,quantity)
            VALUES(%s,%s,%s,%s)
        """, (
            request.form['title'],
            request.form['author'],
            request.form['category'],
            request.form['quantity']
        ))

        mysql.connection.commit()
        cursor.close()
        return redirect('/books')

    return render_template("add_books.html")

@app.route('/check_session')
def check_session():
    return f"""
    User ID = {session.get('user_id')} <br>
    Username = {session.get('username')} <br>
    Role = {session.get('role')}
    """


@app.route('/edit_book/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_book(id):

    cursor = mysql.connection.cursor()

    if request.method == 'POST':

        cursor.execute("""
            UPDATE books
            SET
            book_name=%s,
            author=%s,
            category=%s,
            quantity=%s
            WHERE book_id=%s
        """, (
            request.form['title'],
            request.form['author'],
            request.form['category'],
            request.form['quantity'],
            id
        ))

        mysql.connection.commit()
        cursor.close()

        return redirect('/books')

    cursor.execute(
        "SELECT * FROM books WHERE book_id=%s",
        (id,)
    )

    data = cursor.fetchone()

    cursor.close()

    if not data:
        return "Book Not Found"

    book = {
        "id": data[0],
        "title": data[1],
        "author": data[2],
        "category": data[3],
        "quantity": data[4],
        "available_quantity": data[5],
        "image": data[9]
    }

    return render_template(
        "edit_books.html",
        book=book
    )




@app.route('/delete-book/<int:book_id>')
@admin_required
def delete_book(book_id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        "DELETE FROM books WHERE book_id=%s",
        (book_id,)
    )

    mysql.connection.commit()

    cursor.close()

    flash("Book deleted successfully!", "success")

    return redirect(url_for('books'))

# MEMBERS
@app.route('/member')
def member():

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM members")
    data = cursor.fetchall()
    cursor.close()

    members = []

    for m in data:
        members.append({
            "id": m[0],
            "admission_no": m[1],
            "full_name": m[2],
            "email": m[3],
            "phone": m[4],
            "gender": m[5],
            "course": m[6],
            "address": m[7],
            "join_date": m[8]
        })

    return render_template("member.html", members=members)

@app.route('/add_member', methods=['GET', 'POST'])
@admin_required
def add_member():

    if request.method == 'POST':

        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO members(
                admission_no,
                full_name,
                email,
                phone,
                gender,
                course,
                address,
                join_date
            )
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            request.form['admission_no'],
            request.form['full_name'],
            request.form['email'],
            request.form['phone'],
            request.form['gender'],
            request.form['course'],
            request.form['address'],
            request.form['join_date']
        ))

        mysql.connection.commit()
        cursor.close()

        return redirect('/members')

    return render_template('add_member.html')


@app.route('/edit_member/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_member(id):
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        cursor.execute("""
            UPDATE members
            SET
            admission_no=%s,
            full_name=%s,
            email=%s,
            phone=%s,
            gender=%s,
            course=%s,
            address=%s,
            join_date=%s
            WHERE member_id=%s
        """,
        (
        request.form["admission_no"],
        request.form["full_name"],
        request.form["email"],
        request.form["phone"],
        request.form["gender"],
        request.form["course"],
        request.form["address"],
        request.form["join_date"],
        id
        ))

        mysql.connection.commit()
        cursor.close()
        return redirect('/member')

    cursor.execute("SELECT * FROM members WHERE member_id=%s", (id,))
    data = cursor.fetchone()
    cursor.close()

    member = {
        "id": data[0],
        "name": data[1],
        "email": data[2],
        "phone": data[3],
        "join_date": data[4]
    }

    return render_template("edit_member.html", member=member)


@app.route('/delete_member/<int:id>')
@admin_required
def delete_member(id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        "DELETE FROM members WHERE member_id=%s",
        (id,)
    )

    mysql.connection.commit()
    cursor.close()

    return redirect('/member')

# ================= ISSUE BOOK =================
@app.route('/issue_books', methods=['GET', 'POST'])
def issue_books():

    cursor = mysql.connection.cursor()

    if request.method == 'POST':

        cursor.execute("""
        INSERT INTO issued_books
        (book_id, member_id, issue_date, status)
        VALUES (%s,%s,%s,'Issued')
        """, (
            request.form['book_id'],
            request.form['member_id'],
            request.form['issue_date']
        ))

        mysql.connection.commit()

        return redirect('/dashboard')

    cursor.execute("""
        SELECT book_id, book_name
        FROM books
        WHERE available_quantity > 0
    """)

    books = cursor.fetchall()

    cursor.execute("""
        SELECT member_id, full_name
        FROM members
    """)

    members = cursor.fetchall()

    return render_template(
        "issue_books.html",
        books=books,
        members=members
    )

# ================= RETURN BOOK =================
@app.route('/return_book', methods=['GET', 'POST'])
def return_book():

    cursor = mysql.connection.cursor()

    if request.method == 'POST':

        cursor.execute("""
            UPDATE issued_books
            SET return_date=%s,
                status='Returned'
            WHERE issue_id=%s
        """, (
            request.form['return_date'],
            request.form['issue_id']
        ))

        mysql.connection.commit()
        cursor.close()

        return redirect('/dashboard')

    cursor.execute("""
        SELECT
            ib.issue_id,
            b.title,
            m.full_name,
            ib.issue_date
        FROM issued_books ib
        JOIN books b
            ON ib.book_id = b.book_id
        JOIN members m
            ON ib.member_id = m.member_id
        WHERE ib.status='Issued'
    """)

    data = cursor.fetchall()
    cursor.close()

    issued_books = []

    for r in data:
        issued_books.append({
            "id": r[0],
            "book_title": r[1],
            "member_name": r[2],
            "issue_date": r[3]
        })

    return render_template(
        "return_book.html",
        issued_books=issued_books
    )
# ================= ATTENDANCE =================
@app.route('/attendance', methods=['GET','POST'])
@login_required
def attendance():
    pass

    cursor = mysql.connection.cursor()

    if request.method == 'POST':

        cursor.execute("""
        INSERT INTO attendance(
            member_id,
            attendance_date,
            check_in_time,
            check_out_time,
            status
        )
        VALUES(%s,%s,%s,%s,%s)
        """,(
            request.form['member_id'],
            request.form['attendance_date'],
            request.form['check_in_time'],
            request.form['check_out_time'],
            request.form['status']
        ))

        mysql.connection.commit()

        return redirect('/attendance_report')

    cursor.execute("""
        SELECT member_id,
               admission_no,
               full_name
        FROM members
    """)

    members = cursor.fetchall()

    return render_template(
        "attendance.html",
        members=members
    )

@app.route('/attendance_report')
@admin_required
def attendance_report():

    cursor = mysql.connection.cursor()

    cursor.execute("""
    SELECT
        a.attendance_id,
        m.full_name,
        a.attendance_date,
        a.status,
        a.check_in_time,
        a.check_out_time
    FROM attendance a
    JOIN members m
        ON a.member_id = m.member_id
    ORDER BY a.attendance_date DESC
    """)

    records = cursor.fetchall()

    cursor.close()

    return render_template(
        "attendance_report.html",
        records=records
    )
# ================= NOTICES =================
@app.route('/notices')
def notices():

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM notices ORDER BY date DESC")
    data = cursor.fetchall()
    cursor.close()

    notices = []
    for n in data:
        notices.append({
            "id": n[0],
            "title": n[1],
            "message": n[2],
            "date": n[3]
        })

    return render_template("notices.html", notices=notices)


@app.route('/add_notice', methods=['GET', 'POST'])
@admin_required
def add_notice():

    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        cursor.execute("""
            INSERT INTO notices(title,message,date)
            VALUES(%s,%s,%s)
        """, (
            request.form['title'],
            request.form['message'],
            request.form['date']
        ))

        mysql.connection.commit()
        cursor.close()
        return redirect('/notices')

    return render_template("add_notice.html")

# ================= CHATBOT =================
@app.route('/chatbot', methods=['GET', 'POST'])
@login_required
def chatbot():
    pass

    if 'chats' not in session:
        session['chats'] = []

    if request.method == 'POST':

        msg = request.form['message'].strip().lower()

        cur = mysql.connection.cursor()

        # Total Books

        if "total books" in msg:

            cur.execute("SELECT COUNT(*) FROM books")

            total = cur.fetchone()[0]

            reply = f"Total Books Available: {total}"

        # Total Members

        elif "total members" in msg:

            cur.execute("SELECT COUNT(*) FROM members")

            total = cur.fetchone()[0]

            reply = f"Total Members: {total}"

        # Issued Books

        elif "issued books" in msg:

            cur.execute("""
                SELECT COUNT(*)
                FROM issued_books
                WHERE status='Issued'
            """)

            total = cur.fetchone()[0]

            reply = f"Currently Issued Books: {total}"

        # Return Books

        elif "return book" in msg:

            reply = "Go to Return Book page to return books."

        # Attendance

        elif "attendance" in msg:

            cur.execute("""
                SELECT COUNT(*)
                FROM attendance
                WHERE status='Present'
            """)

            total = cur.fetchone()[0]

            reply = f"Present Students Today: {total}"

        # Fine

        elif "fine" in msg:

            cur.execute("""
                SELECT SUM(fine_amount)
                FROM issued_books
            """)

            fine = cur.fetchone()[0]

            if fine is None:
                fine = 0

            reply = f"Total Fine Amount: ₹{fine}"

        # Notice

        elif "notice" in msg:

            cur.execute("""
                SELECT title
                FROM notices
                ORDER BY id DESC
                LIMIT 1
            """)

            notice = cur.fetchone()

            if notice:
                reply = f"Latest Notice: {notice[0]}"
            else:
                reply = "No notices available."

        # Dashboard

        elif "dashboard" in msg:

            reply = "Dashboard contains books, members, attendance, notices and analytics."

        # Library Timing

        elif "timing" in msg:

            reply = "Library Timing: 9:00 AM to 6:00 PM"

        # Help

        elif "help" in msg:

            reply = """
Available Commands:

1. Total Books
2. Total Members
3. Issued Books
4. Attendance
5. Fine
6. Latest Notice
7. Library Timing
8. Dashboard
            """

        else:

            reply = """
Sorry, I didn't understand.

Try:
- Total Books
- Total Members
- Attendance
- Fine
- Library Timing
- Latest Notice
- Help
            """

        cur.close()

        session['chats'].append({
            "user": msg,
            "bot": reply
        })

        session.modified = True

    return render_template(
        "chatbot.html",
        chats=session.get('chats', [])
    )


# ================= ANALYTICS =================
from datetime import datetime
from ml.demand import predict_book_demand, recommend_purchase
@app.route('/analytics')
@admin_required
def analytics():

    cursor = mysql.connection.cursor()

    # ============================
    # Dashboard Counts
    # ============================

    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM members")
    total_members = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM issued_books
        WHERE status='Issued'
    """)
    issued_books = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM issued_books
        WHERE status='Returned'
    """)
    returned_books = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE status='Present'
    """)
    present_members = cursor.fetchone()[0]

    cursor.execute("""
        SELECT IFNULL(SUM(fine_amount),0)
        FROM issued_books
    """)
    total_fine = cursor.fetchone()[0]

    # ==========================================
    # ML Demand Prediction
    # ==========================================

    cursor.execute("""

        SELECT

            b.book_id,
            b.book_name,
            b.available_quantity,

            COUNT(i.issue_id) AS total_issues,

            SUM(

                CASE

                WHEN i.issue_date >= DATE_SUB(CURDATE(),INTERVAL 30 DAY)

                THEN 1

                ELSE 0

                END

            ) AS recent_issues

        FROM books b

        LEFT JOIN issued_books i

        ON b.book_id=i.book_id

        GROUP BY b.book_id

    """)

    books = cursor.fetchall()

    current_month = datetime.now().month

    highest_demand = -1

    predicted_book = "No Data"

    expected_demand = 0

    restock = "NO"

    confidence = 95

    for row in books:

        book_id = row[0]

        book_name = row[1]

        available_quantity = row[2] if row[2] else 0

        total_issues = row[3] if row[3] else 0

        recent_issues = row[4] if row[4] else 0

        demand = predict_book_demand(

            book_id=book_id,

            month_no=current_month,

            total_issues=total_issues,

            recent_issues=recent_issues,

            available_quantity=available_quantity

        )

        if demand > highest_demand:

            highest_demand = demand

            predicted_book = book_name

            expected_demand = demand

            status, purchase = recommend_purchase(

                demand,

                available_quantity

            )

            restock = status

    cursor.close()

    return render_template(

        "analytics.html",

        total_books=total_books,

        total_members=total_members,

        issued_books=issued_books,

        returned_books=returned_books,

        present_members=present_members,

        total_fine=total_fine,

        predicted_book=predicted_book,

        expected_demand=expected_demand,

        restock=restock,

        confidence=confidence

    )
    

# ================= LOGIN =================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        

        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT * FROM users
            WHERE username=%s AND password=%s
        """, (username, password))

        user = cursor.fetchone()

        if user:

            print(user)
            print("ROLE =", user[4])

            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = str(user[4]).strip().lower()

            return redirect('/dashboard')

        return render_template('login.html', error='Invalid Login')

    return render_template('login.html')

# ================= REGISTER =================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', 'student').strip()
        address = request.form.get('address', '').strip()

        # Debug
        print("FORM DATA =", request.form)

        if username == '':
            return "Username field missing"

        if password == '':
            return "Password field missing"

        cursor = mysql.connection.cursor()

        # Username already exists check
        cursor.execute(
            "SELECT * FROM users WHERE username=%s",
            (username,)
        )

        user = cursor.fetchone()

        if user:
            cursor.close()
            return "Username already exists"

        cursor.execute("""
            INSERT INTO users
            (
                username,
                email,
                password,
                role,
                address
            )
            VALUES (%s,%s,%s,%s,%s)
        """, (
            username,
            email,
            password,
            role,
            address
        ))

        mysql.connection.commit()
        cursor.close()

        return redirect('/login')

    return render_template('register.html')

@app.route('/pay_fee', methods=['GET', 'POST'])
def pay_fee():

    cursor = mysql.connection.cursor()

    if request.method == 'POST':

        admission_no = request.form['admission_no']

        cursor.execute("""
            SELECT member_id, full_name
            FROM members
            WHERE admission_no=%s
        """, (admission_no,))

        member = cursor.fetchone()

        if not member:
            return "Member Not Found"

        member_id = member[0]

        cursor.execute("""
            INSERT INTO fees(
                member_id,
                admission_no,
                member_name,
                amount,
                payment_date,
                payment_method,
                status
            )
            VALUES(%s,%s,%s,%s,%s,%s,%s)
        """, (
            member_id,
            request.form['admission_no'],
            request.form['member_name'],
            request.form['amount'],
            request.form['payment_date'],
            request.form['payment_method'],
            request.form['status']
        ))

        mysql.connection.commit()
        cursor.close()

        return redirect('/fee_history')

    return render_template('pay_fee.html')

@app.route('/fee_history')
def fee_history():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
        f.fee_id,
        m.admission_no,
        m.full_name,
        f.amount,
        f.payment_date,
        f.payment_method,
        f.status
        FROM fees f
        JOIN members m
        ON f.member_id = m.member_id
        ORDER BY f.fee_id DESC
    """)

    records = cursor.fetchall()

    cursor.close()

    return render_template(
        'fee_history.html',
        records=records
    )

@app.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO contacts (name, email, phone, message)
            VALUES (%s, %s, %s, %s)
        """, (name, email, phone, message))

        mysql.connection.commit()
        cursor.close()

        return "Message Sent Successfully"

    return render_template("contact.html")


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/<service>')
def service_page(service):
    return render_template('service.html', service=service.replace('_', ' ').title())


@app.route("/careers")
def careers():
    return render_template("careers.html")


import os
from werkzeug.utils import secure_filename
from flask import request

UPLOAD_FOLDER = "static/resumes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/apply-career", methods=["POST"])
def apply_career():

    name = request.form["name"]
    email = request.form["email"]
    position = request.form["position"]

    file = request.files["resume"]
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    return "Application Submitted Successfully 🚀"

@app.route("/academic_learning")
def academic_learning():

    courses = [

        {
            "id":1,
            "name":"python",
            "title":"Python Programming",
            "image":"python.jpg"
        },

        {
            "id":2,
            "name":"machine_learning",
            "title":"Machine Learning",
            "image":"machinelearning.jpg"
        },

        {
            "id":3,
            "name":"database",
            "title":"Database Management",
            "image":"database.jpg"
        }

    ]

    return render_template(
        "academic_learning.html",
        courses=courses
    )



import uuid

@app.route("/certificate/<course>")
def certificate(course):

    student_name = session.get("name", "Student")

    course_name = course.replace("_", " ").title()

    certificate_id = str(uuid.uuid4())[:8].upper()

    completion_date = datetime.now().strftime("%d %B %Y")

    return render_template(
        "certificate.html",
        student_name=student_name,
        course_name=course_name,
        completion_date=completion_date,
        certificate_id=certificate_id,
        grade="A+"
    )

@app.route("/update_progress/<course>/<int:value>")
def update_progress(course, value):

    user_id = session["user_id"]

    # update DB logic here

    return "Progress Updated"

@app.route("/quiz/<course>")
def quiz(course):

    return render_template(
        "quiz.html",
        course=course
    )

@app.route("/course/<course_name>")
def course_details(course_name):

    data={

        "python":{

            "title":"Python Programming",

            "description":"Complete Python Course",

            "video":"https://www.youtube.com/embed/rfscVS0vtbw",

            "notes":"python_notes.pdf",

            "completed":False

        },

        "machine_learning":{

            "title":"Machine Learning",

            "description":"ML Basics",

            "video":"https://www.youtube.com/embed/GwIo3gDZCVQ",

            "notes":"ml_notes.pdf",

            "completed":False

        },

        "database":{

            "title":"Database Management",

            "description":"SQL & DBMS",

            "video":"https://www.youtube.com/embed/HXV3zeQKqGY",

            "notes":"dbms_notes.pdf",

            "completed":True

        }

    }

    return render_template(
        "course_details.html",
        course=data[course_name]
    )
# ================= LOGOUT =================

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
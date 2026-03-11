from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db, mysql
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
init_db(app)

# ---------------- LOGIN REQUIRED ----------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first!', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ---------------- HOME ----------------
@app.route('/')
def index():
    return redirect(url_for('login'))

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        # Student login
        cur.execute("SELECT * FROM Students WHERE Email=%s AND Password=%s",(email,password))
        student = cur.fetchone()

        if student:
            session['user_id'] = student['Student_ID']
            session['user_email'] = student['Email']
            session['user_name'] = student['Name']
            session['user_type'] = 'student'
            flash('Login successful!','success')
            cur.close()
            return redirect(url_for('student_dashboard'))

        # Admin login
        cur.execute("SELECT * FROM Admin WHERE Email=%s AND Password=%s",(email,password))
        admin = cur.fetchone()
        cur.close()

        if admin:
            session['user_id'] = admin['Admin_ID']
            session['user_email'] = admin['Email']
            session['user_name'] = admin['Name']
            session['user_type'] = 'admin'
            flash('Login successful!','success')
            return redirect(url_for('admin_dashboard'))

        flash('Invalid email or password!','error')

    return render_template('login.html')

# ---------------- STUDENT DASHBOARD ----------------
@app.route('/student/dashboard')
@login_required
def student_dashboard():

    if session['user_type']!='student':
        flash('Access denied!','error')
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT s.*, c.Course_Name, c.Fee
    FROM Students s
    LEFT JOIN Courses c ON s.Course_ID=c.Course_ID
    WHERE s.Student_ID=%s
    """,(session['user_id'],))

    student = cur.fetchone()

    cur.execute("SELECT * FROM Payments WHERE Student_ID=%s ORDER BY Payment_Date DESC",(session['user_id'],))
    payments = cur.fetchall()

    cur.execute("SELECT * FROM Installments WHERE Student_ID=%s ORDER BY Due_Date",(session['user_id'],))
    installments = cur.fetchall()

    cur.execute("SELECT * FROM Scholarships WHERE Student_ID=%s",(session['user_id'],))
    scholarship = cur.fetchone()

    cur.close()

    return render_template(
        'student_dashboard.html',
        student=student,
        payments=payments,
        installments=installments,
        scholarship=scholarship
    )

# ---------------- ADMIN DASHBOARD ----------------
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():

    if session['user_type']!='admin':
        flash('Access denied!','error')
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) AS total FROM Students")
    total_students = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS total FROM Courses")
    total_courses = cur.fetchone()['total']

    cur.execute("SELECT SUM(Amount_Paid) AS total FROM Payments")
    total_collections = cur.fetchone()['total'] or 0

    cur.execute("SELECT COUNT(*) AS total FROM Installments WHERE Status='Pending'")
    pending_installments = cur.fetchone()['total']

    cur.execute("SELECT s.*,c.Course_Name FROM Students s LEFT JOIN Courses c ON s.Course_ID=c.Course_ID")
    students = cur.fetchall()

    cur.execute("SELECT * FROM Courses")
    courses = cur.fetchall()

    cur.execute("""
    SELECT p.*,s.Name AS Student_Name
    FROM Payments p
    JOIN Students s ON p.Student_ID=s.Student_ID
    ORDER BY p.Payment_Date DESC LIMIT 10
    """)
    payments = cur.fetchall()

    cur.execute("""
    SELECT i.*,s.Name AS Student_Name
    FROM Installments i
    JOIN Students s ON i.Student_ID=s.Student_ID
    ORDER BY i.Due_Date
    """)
    installments = cur.fetchall()

    cur.close()

    return render_template(
        'admin_dashboard.html',
        total_students=total_students,
        total_courses=total_courses,
        total_collections=total_collections,
        pending_installments=pending_installments,
        students=students,
        courses=courses,
        payments=payments,
        installments=installments
    )

# ---------------- ADD STUDENT ----------------
@app.route('/add_student', methods=['POST'])
@login_required
def add_student():

    if session['user_type']!='admin':
        return redirect(url_for('login'))

    name=request.form['name']
    email=request.form['email']
    password=request.form['password']
    phone=request.form.get('phone')
    course_id=request.form.get('course_id')

    if not course_id:
        flash('Please select a course!','error')
        return redirect(url_for('admin_dashboard'))

    cur=mysql.connection.cursor()

    try:

        cur.execute("""
        INSERT INTO Students
        (Name,Email,Password,Phone,Course_ID,Status)
        VALUES(%s,%s,%s,%s,%s,'Active')
        """,(name,email,password,phone,course_id))

        mysql.connection.commit()

        student_id = cur.lastrowid

        cur.execute("SELECT Fee FROM Courses WHERE Course_ID=%s",(course_id,))
        course = cur.fetchone()

        if course:

            total_fee = course['Fee']

            # -------- MAX 2 INSTALLMENTS --------
            duration = 2
            installment_amount = total_fee / duration
            # ------------------------------------

            for i in range(1, duration+1):

                cur.execute("""
                INSERT INTO Installments
                (Student_ID,Installment_No,Due_Date,Installment_Amount,Status)
                VALUES(%s,%s,DATE_ADD(CURDATE(), INTERVAL %s MONTH),%s,'Pending')
                """,(student_id,i,i,installment_amount))

            mysql.connection.commit()

        flash('Student added successfully!','success')

    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error adding student: {str(e)}','error')

    finally:
        cur.close()

    return redirect(url_for('admin_dashboard'))

# ---------------- EDIT STUDENT ----------------
@app.route('/edit_student/<int:student_id>', methods=['GET','POST'])
@login_required
def edit_student(student_id):

    if session['user_type']!='admin':
        flash('Access denied!','error')
        return redirect(url_for('login'))

    cur=mysql.connection.cursor()

    if request.method=='POST':

        name=request.form['name']
        email=request.form['email']
        phone=request.form.get('phone')
        course_id=request.form.get('course_id')

        cur.execute("""
        UPDATE Students
        SET Name=%s,Email=%s,Phone=%s,Course_ID=%s
        WHERE Student_ID=%s
        """,(name,email,phone,course_id,student_id))

        mysql.connection.commit()
        cur.close()

        flash("Student updated successfully","success")
        return redirect(url_for('admin_dashboard'))

    cur.execute("SELECT * FROM Students WHERE Student_ID=%s",(student_id,))
    student = cur.fetchone()

    cur.execute("SELECT * FROM Courses")
    courses = cur.fetchall()

    cur.close()

    return render_template("edit_student.html",student=student,courses=courses)

# ---------------- DELETE STUDENT ----------------
@app.route('/delete_student/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):

    cur=mysql.connection.cursor()

    cur.execute("DELETE FROM Installments WHERE Student_ID=%s",(student_id,))
    cur.execute("DELETE FROM Payments WHERE Student_ID=%s",(student_id,))
    cur.execute("DELETE FROM Students WHERE Student_ID=%s",(student_id,))

    mysql.connection.commit()
    cur.close()

    flash("Student deleted successfully","success")

    return redirect(url_for('admin_dashboard'))

# ---------------- ADD COURSE ----------------
@app.route('/add_course', methods=['POST'])
@login_required
def add_course():

    course_name=request.form['course_name']
    fee=request.form['fee']
    duration=request.form['duration']

    cur=mysql.connection.cursor()

    cur.execute("""
    INSERT INTO Courses(Course_Name,Fee,Duration)
    VALUES(%s,%s,%s)
    """,(course_name,fee,duration))

    mysql.connection.commit()
    cur.close()

    flash("Course added successfully","success")

    return redirect(url_for('admin_dashboard'))

# ---------------- ADD PAYMENT ----------------
# ---------------- ADD PAYMENT ----------------
@app.route('/add_payment', methods=['POST'])
@login_required
def add_payment():

    student_id = request.form['student_id']
    installment_no = request.form['installment_no']
    amount_paid = request.form['amount_paid']
    payment_date = request.form['payment_date']
    payment_mode = request.form['payment_mode']
    remaining_balance = request.form['remaining_balance']

    cur = mysql.connection.cursor()

    try:

        # Insert payment
        cur.execute("""
        INSERT INTO Payments
        (Student_ID,Installment_No,Amount_Paid,Payment_Date,Payment_Mode,Remaining_Balance)
        VALUES(%s,%s,%s,%s,%s,%s)
        """,(student_id,installment_no,amount_paid,payment_date,payment_mode,remaining_balance))

        # -------- UPDATE INSTALLMENT STATUS --------
        cur.execute("""
        UPDATE Installments
        SET Status='Paid'
        WHERE Student_ID=%s AND Installment_No=%s
        """,(student_id,installment_no))
        # -------------------------------------------

        mysql.connection.commit()

        flash("Payment added successfully and installment marked as Paid","success")

    except Exception as e:

        mysql.connection.rollback()
        flash(f"Error adding payment: {str(e)}","error")

    finally:
        cur.close()
    return redirect(url_for('admin_dashboard'))

# ---------------- ADD INSTALLMENT ----------------
@app.route('/add_installment', methods=['POST'])
@login_required
def add_installment():

    student_id=request.form['student_id']
    installment_no=request.form['installment_no']
    due_date=request.form['due_date']
    installment_amount=request.form['installment_amount']
    status=request.form['status']

    cur=mysql.connection.cursor()

    cur.execute("""
    INSERT INTO Installments
    (Student_ID,Installment_No,Due_Date,Installment_Amount,Status)
    VALUES(%s,%s,%s,%s,%s)
    """,(student_id,installment_no,due_date,installment_amount,status))

    mysql.connection.commit()
    cur.close()

    flash("Installment added successfully","success")

    return redirect(url_for('admin_dashboard'))

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!','success')
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True)
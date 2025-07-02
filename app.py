from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create DB and Table if not exist
def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    department TEXT NOT NULL,
                    phone TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

# Home / Registration page
@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        department = request.form.get("department")
        phone = request.form.get("phone")

        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("INSERT INTO students (name, email, department, phone) VALUES (?, ?, ?, ?)",
                  (name, email, department, phone))
        conn.commit()
        conn.close()

        return redirect("/students")

    return render_template("index.html")

# Students List Page
@app.route("/students")
def students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    student_list = c.fetchall()
    conn.close()

    return render_template("students.html", students=student_list)

if __name__ == "__main__":
    app.run(debug=True)

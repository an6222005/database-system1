from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# 連線到 MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="A131984247",
    database="web_demo"
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/insert', methods=['POST'])
def insert():
    student_id = request.form['student_id']
    name = request.form['name']
    age = request.form['age']
    email = request.form['email']

    cursor.execute(
        "INSERT INTO students (student_id, name, age, email) VALUES (%s, %s, %s, %s)",
        (student_id, name, age, email)
    )
    db.commit()
    return "✅ 資料新增成功！"

if __name__ == '__main__':
    app.run(debug=True)

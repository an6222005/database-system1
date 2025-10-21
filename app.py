from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# 連線到 MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="A131984247",
    database="web_demo"
)
cursor = db.cursor(dictionary=True)  # 使用 dictionary=True 方便取欄位名稱

@app.route('/')
def index():
    # READ：讀取所有學生資料
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template("index.html", students=students)

@app.route('/insert', methods=['POST'])
def insert():
    # CREATE：新增學生資料
    student_id = request.form['student_id']
    name = request.form['name']
    age = request.form['age']
    email = request.form['email']

    cursor.execute(
        "INSERT INTO students (student_id, name, age, email) VALUES (%s, %s, %s, %s)",
        (student_id, name, age, email)
    )
    db.commit()
    return redirect('/')  # 新增完回到首頁顯示結果

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    # UPDATE：更新學生資料
    name = request.form['name']
    age = request.form['age']
    email = request.form['email']

    cursor.execute(
        "UPDATE students SET name=%s, age=%s, email=%s WHERE id=%s",
        (name, age, email, id)
    )
    db.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    # DELETE：刪除學生資料
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    db.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

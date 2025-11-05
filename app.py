from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import os

app = Flask(__name__)

# Connect to MongoDB Atlas
MONGO_URI = "mongodb+srv://linchenan:<A131984247@cluster0.n2o4iqb.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['student_db']
collection = db['students']

# Home page - show students
@app.route('/')
def index():
    students = list(collection.find())
    return render_template("index.html", students=students)

# Insert a single student
@app.route('/insert', methods=['POST'])
def insert():
    student = {
        'name': request.form['name'],
        'age': int(request.form['age']),
        'email': request.form['email']
    }
    collection.insert_one(student)
    return redirect('/')

# Insert many predefined students
@app.route('/insert_many')
def insert_many():
    predefined_students = [
        {"name": "Alice", "age": 20, "email": "alice@example.com"},
        {"name": "Bob", "age": 21, "email": "bob@example.com"},
        {"name": "Charlie", "age": 22, "email": "charlie@example.com"}
    ]
    collection.insert_many(predefined_students)
    return redirect('/')

# Delete a student by ID
@app.route('/delete/<student_id>')
def delete(student_id):
    from bson.objectid import ObjectId
    collection.delete_one({"_id": ObjectId(student_id)})
    return redirect('/')

if __name__ == '__main__':
    # Bind to Render port
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

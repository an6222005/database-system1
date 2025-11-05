from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# ⚠️ 替換成你自己的 MongoDB 連線字串
# 範例: mongodb+srv://<username>:<password>@cluster0.n2o4iqb.mongodb.net/?retryWrites=true&w=majority
client = MongoClient("mongodb+srv://linchenan:A131984247@cluster0.n2o4iqb.mongodb.net/?appName=Cluster0")
db = client["student_db"]
collection = db["students"]

@app.route("/")
def index():
    students = list(collection.find())
    return render_template("mongo.html", students=students)

@app.route("/insert_many", methods=["POST"])
def insert_many():
    sample_students = [
        {"name": "Alice", "age": 20, "email": "alice@example.com"},
        {"name": "Bob", "age": 21, "email": "bob@example.com"},
        {"name": "Charlie", "age": 22, "email": "charlie@example.com"}
    ]
    collection.insert_many(sample_students)
    return redirect(url_for("index"))

@app.route("/add_student", methods=["POST"])
def add_student():
    name = request.form.get("name")
    age = request.form.get("age")
    email = request.form.get("email")
    if name and age and email:
        collection.insert_one({"name": name, "age": int(age), "email": email})
    return redirect(url_for("index"))

@app.route("/delete/<string:email>", methods=["POST"])
def delete_student(email):
    collection.delete_one({"email": email})
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

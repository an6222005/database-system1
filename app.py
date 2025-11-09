from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# MongoDB 連線設定
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://linchenan:A131984247@cluster0.n2o4iqb.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client.student_db
collection = db.students  # collection 名稱

# 首頁顯示所有學生
@app.route("/")
def index():
    students = list(collection.find())
    return render_template("index.html", students=students)

# 新增單筆學生
@app.route("/insert", methods=["POST"])
def insert():
    name = request.form.get("name")
    age = int(request.form.get("age"))
    email = request.form.get("email")
    collection.insert_one({"name": name, "age": age, "email": email})
    return redirect("/")

# Insert Many 預設學生
@app.route("/insert_many", methods=["POST"])
def insert_many():
    predefined_students = [
        {"name": "Alice", "age": 20, "email": "alice@example.com"},
        {"name": "Bob", "age": 21, "email": "bob@example.com"},
        {"name": "Charlie", "age": 22, "email": "charlie@example.com"}
    ]
    collection.insert_many(predefined_students)
    return redirect("/")

# 修改學生
@app.route("/update/<id>", methods=["POST"])
def update(id):
    name = request.form.get("name")
    age = int(request.form.get("age"))
    email = request.form.get("email")
    collection.update_one({"_id": ObjectId(id)}, {"$set": {"name": name, "age": age, "email": email}})
    return redirect("/")

# 刪除學生
@app.route("/delete/<id>")
def delete(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

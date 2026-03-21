from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import os

app = Flask(__name__)

# ==============================
# 📁 Upload Folder
# ==============================
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ==============================
# 🔐 MongoDB (Use ENV Variable in Render)
# ==============================
client = MongoClient("mongodb+srv://vijaysuryawanshi7224_db_user:vijay%402005@cluster0.ckvnjfm.mongodb.net/collegedb?retryWrites=true&w=majority") 

db = client["student_db"]
collection = db["documents"]
# ==============================
# 🏠 Home Page
# ==============================
@app.route('/')
def index():
    files = list(collection.find())
    return render_template('index.html', files=files)

# ==============================
# 📤 Upload
# ==============================
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(filepath)

    collection.insert_one({
        "filename": filename
    })

    return redirect(url_for('index'))

# ==============================
# 👁️ View File
# ==============================
@app.route('/view/<filename>')
def view_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ==============================
# ❌ Delete
# ==============================
@app.route('/delete/<filename>')
def delete(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(filepath):
        os.remove(filepath)

    collection.delete_one({"filename": filename})
    return redirect(url_for('index'))

# ==============================
# ▶️ Run
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
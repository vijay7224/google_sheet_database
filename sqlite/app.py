from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import os

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MongoDB Connection
client = MongoClient("mongodb+srv://vijaysuryawanshi7224_db_user:vijay%402005@cluster0.ckvnjfm.mongodb.net/collegedb?retryWrites=true&w=majority") 

db = client["student_db"]
collection = db["documents"]

# Home Page
@app.route('/')
def index():
    files = list(collection.find())
    return render_template('index.html', files=files)

# Upload Route
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

    # Save to MongoDB
    collection.insert_one({
        "filename": filename
    })

    return redirect(url_for('index'))

# Delete File
@app.route('/delete/<filename>')
def delete(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(filepath):
        os.remove(filepath)

    collection.delete_one({"filename": filename})
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
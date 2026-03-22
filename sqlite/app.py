from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import cloudinary
import cloudinary.uploader
import os

app = Flask(__name__)

# ==============================
# ☁️ Cloudinary Config
# ==============================
cloudinary.config(
    cloud_name = os.getenv("CLOUD_NAME"),
    api_key = os.getenv("API_KEY"),
    api_secret = os.getenv("API_SECRET")
)

# ==============================
# 🔐 MongoDB Config
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
# 📤 Upload File (Cloudinary)
# ==============================
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')

    if not file or file.filename == '':
        return "❌ No file selected"

    try:
        result = cloudinary.uploader.upload(file)

        file_url = result['secure_url']
        public_id = result['public_id']

        collection.insert_one({
            "filename": file.filename,
            "url": file_url,
            "public_id": public_id
        })

    except Exception as e:
        return f"Upload failed: {str(e)}"

    return redirect(url_for('index'))

# ==============================
# ❌ Delete File (Cloudinary + DB)
# ==============================
@app.route('/delete/<id>')
def delete(id):
    try:
        file = collection.find_one({"_id": ObjectId(id)})

        if file:
            cloudinary.uploader.destroy(file['public_id'])
            collection.delete_one({"_id": ObjectId(id)})

    except Exception as e:
        return f"Delete failed: {str(e)}"

    return redirect(url_for('index'))

# ==============================
# ▶️ Run App
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
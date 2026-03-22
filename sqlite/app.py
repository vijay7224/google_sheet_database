from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import cloudinary
import cloudinary.uploader
import os

app = Flask(__name__)

# Allowed file types
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Cloudinary Config
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

# MongoDB Config
client = MongoClient("mongodb+srv://vijaysuryawanshi7224_db_user:vijay%402005@cluster0.ckvnjfm.mongodb.net/collegedb?retryWrites=true&w=majority") 

db = client["student_db"]
collection = db["documents"]
# ------------------------------
# Home Page
# ------------------------------
@app.route('/')
def index():
    files = list(collection.find())
    return render_template('index.html', files=files)

# ------------------------------
# Upload File
# ------------------------------
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file or file.filename == '':
        return "❌ No file selected"

    if not allowed_file(file.filename):
        return "❌ Only PDF, JPG, PNG allowed"

    ext = file.filename.rsplit('.', 1)[1].lower()
    resource_type = "raw" if ext == "pdf" else "image"

    result = cloudinary.uploader.upload(file, resource_type=resource_type)

    file_url = result['secure_url']
    if ext == "pdf" and not file_url.endswith(".pdf"):
        file_url += ".pdf"

    collection.insert_one({
        "filename": file.filename,
        "url": file_url,
        "public_id": result['public_id'],
        "type": ext
    })

    return redirect(url_for('index'))

# ------------------------------
# View File (PDF.js / Image)
# ------------------------------
@app.route('/view/<id>')
def view_file(id):
    file = collection.find_one({"_id": ObjectId(id)})
    if not file:
        return "File not found"
    return render_template("view.html", file=file)

# ------------------------------
# Delete File
# ------------------------------
@app.route('/delete/<id>')
def delete(id):
    file = collection.find_one({"_id": ObjectId(id)})
    if file:
        resource_type = "raw" if file['type'] == "pdf" else "image"
        cloudinary.uploader.destroy(file['public_id'], resource_type=resource_type)
        collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

# ------------------------------
# Run App (Render-ready)
# ------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
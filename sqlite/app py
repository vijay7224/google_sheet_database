from flask import Flask, request, render_template, send_from_directory
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Google Sheet connection
scope = [
"https://spreadsheets.google.com/feeds",
"https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("user_database").sheet1


@app.route("/")
def home():
    return render_template("form.html")


@app.route("/submit", methods=["POST"])
def submit():

    name = request.form["name"]
    phone = request.form["phone"]
    email = request.form["email"]

    resume = request.files["resume"]

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], resume.filename)
    resume.save(filepath)

    sheet.append_row([name, phone, email, resume.filename])

    return f"""
    <h2>Registration Successful</h2>
    <p>Name: {name}</p>
    <p>Email: {email}</p>

    <a href="/uploads/{resume.filename}" target="_blank">
    <button style="padding:10px 20px;background:#28a745;color:white;border:none;border-radius:5px;">
    View Resume
    </button>
    </a>
    """


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
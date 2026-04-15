from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = 'supersecret_dev_key'

# Create the uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Extension Allowlist
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    # Check if the file has an extension and if it's in the allowed list
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return "No file part in request", 400

        file = request.files['file']

        if file.filename == '':
            return "No selected file", 400

        if file and allowed_file(file.filename):
            # TODO 2: Sanitize the filename. Use secure_filename() from werkzeug.utils.
            # This automatically strips dangerous characters like '../'.
            # However, we will use it primarily to safely extract the extension.
            safe_filename = secure_filename(file.filename)
            file_ext = safe_filename.rsplit('.', 1)[1].lower()

            # TODO 3 & 4: The UUID Sandbox. Completely decouple the file from user input.
            # Generate a random, unique filename. This ensures that even if an attacker
            # provides a malicious name, it is completely ignored. The file is safely
            # trapped in the 'uploads/' folder with a harmless, random name.
            random_filename = str(uuid.uuid4().hex)
            final_filename = f"{random_filename}.{file_ext}"

            # Vulnerable storage execution: (This is the fix)
            # Create the safe, final file path.
            file_path = os.path.join(UPLOAD_FOLDER, final_filename)
            file.save(file_path)

            return f"File successfully uploaded and sandboxed at: {file_path}", 200
        else:
            # TODO 1: Implement an Extension Allowlist. Return a 400 if it's not a safe extension.
            return "Error: File type not allowed. Please upload a .png, .jpg, or .gif file.", 400

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
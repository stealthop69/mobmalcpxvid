from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB setup (use the connection string provided by MongoDB Atlas or Railway)
client = MongoClient(os.getenv("MONGO_URI"))
db = client['file_upload_db']
files_collection = db['files']

# Ensure the 'uploads' folder exists (local uploads folder)
UPLOAD_FOLDER = '/home/your_username/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Store file metadata in MongoDB
    file_data = {
        'file_name': file.filename,
        'file_size': os.path.getsize(file_path),
        'upload_time': 'CURRENT_TIMESTAMP'  # You can store timestamp here or handle it later
    }
    files_collection.insert_one(file_data)

    return jsonify({"message": "File uploaded successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)

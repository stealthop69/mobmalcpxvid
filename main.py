from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
import datetime

app = Flask(__name__)

# MongoDB connection from Railway environment variable
client = MongoClient(os.getenv("MONGO_URI"))
db = client['malware_db']
collection = db['uploads']

# Upload folder (temporary only)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('files')
    device_name = request.form.get('device_name', 'unknown')

    if not files:
        return jsonify({"error": "No files provided"}), 400

    uploaded = []
    for file in files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        file_data = {
            "device_name": device_name,
            "file_name": file.filename,
            "file_size": os.path.getsize(file_path),
            "upload_time": datetime.datetime.utcnow()
        }
        collection.insert_one(file_data)
        uploaded.append(file.filename)

    return jsonify({"message": "Files uploaded", "files": uploaded}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
socketio = SocketIO(app)

BASE_DIR = '/storj-us'  # Make sure this directory exists or change to a valid directory

@app.route('/')
def index():
    files = list_files(BASE_DIR)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file:
        filepath = os.path.join(BASE_DIR, uploaded_file.filename)
        uploaded_file.save(filepath)
        socketio.emit('file_updated', {'message': f'{uploaded_file.filename} uploaded!'})
        return jsonify(success=True, message=f"Uploaded {uploaded_file.filename} successfully!")
    return jsonify(success=False, message="Failed to upload file.")

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    filepath = os.path.join(BASE_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        socketio.emit('file_updated', {'message': f'{filename} deleted!'})
        return jsonify(success=True, message=f"Deleted {filename} successfully!")
    return jsonify(success=False, message=f"File {filename} not found.")

@app.route('/files/<filename>')
def serve_file(filename):
    return send_from_directory(BASE_DIR, filename)

def list_files(startpath):
    return [f for f in os.listdir(startpath) if os.path.isfile(os.path.join(startpath, f))]

if __name__ == '__main__':
    socketio.run(app, debug=False)

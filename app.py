# app.py
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
#load the db host, user, password, and database name from the .env file
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
#set the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?ssl_mode=DISABLED'
db = SQLAlchemy(app)
CORS(app)

# users class model
class User(db.Model):
    #table name is users
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    wallet = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    special_link = db.Column(db.String(8), unique=True, nullable=True)

# folders class model
class Folder(db.Model):
    #table name is content_folders
    __tablename__ = 'content_folders'
    id = db.Column(db.Integer, primary_key=True)
    parent_folder_id = db.Column(db.Integer, db.ForeignKey('content_folders.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #folder name is varchar 255 utf8mb4
    folder_name = db.Column(db.String(255), unique=True, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    visible_folder_name = db.Column(db.String(255), unique=True, nullable=False)

class File(db.Model):
    #db name is "tmp_goodness" and file table is "contents"
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #content name is varchar 255 utf8mb4
    content_name = db.Column(db.String(255), unique=True, nullable=False)
    content_path = db.Column(db.String(255), unique=True, nullable=False)
    #content size is a string from our api
    content_size = db.Column(db.String(255), unique=True, nullable=False)
    status  = db.Column(db.String(255), unique=True, nullable=False)
    content_folder_id = db.Column(db.Integer, db.ForeignKey('content_folders.id'))
    duplicate_source_id = db.Column(db.Integer, db.ForeignKey('contents.id'))
    #our api sets timestamps as null by default
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content_name': self.content_name,
            'content_path': self.content_path,
            'content_size': self.content_size,
            'status': self.status,
            'content_folder_id': self.content_folder_id,
            'duplicate_source_id': self.duplicate_source_id,
            'deleted_at': self.deleted_at,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

@app.route('/files', methods=['GET'])
def get_files():
    files = File.query.all()
    return jsonify([f.serialize for f in files])

@app.route('/files', methods=['POST'])
def upload_file():
    file = request.files['file']
    new_file = File(name=file.filename, type=file.content_type, content=file.read())
    db.session.add(new_file)
    db.session.commit()
    return jsonify(new_file.serialize)

@app.route('/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    file = File.query.get(file_id)
    db.session.delete(file)
    db.session.commit()
    return '', 204


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("frontend/dist/" + path):
        return send_from_directory('frontend/dist', path)
    else:
        return send_from_directory('frontend/dist', 'index.html')
    
if __name__ == '__main__':
    app.run(debug=False)

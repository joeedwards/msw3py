# app.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/dbname'
db = SQLAlchemy()
CORS(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    content = db.Column(db.LargeBinary, nullable=True)

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

if __name__ == '__main__':
    app.run(debug=True)

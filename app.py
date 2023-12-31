# app.py
from flask import Flask, jsonify, request, send_from_directory, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from filemanager import FileManager
from config import ConfigRepository
from web3 import Web3
import os, hashlib, requests


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
ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")
ALCHEMY_API_NFT_URL = os.getenv("ALCHEMY_API_NFT_URL")
ALCHEMY_API_URL = os.getenv("ALCHEMY_API_URL")
w3 = Web3(Web3.HTTPProvider(ALCHEMY_API_URL))
challenges = {}

def generate_challenge(wallet_address):
    challenge = hashlib.sha256(os.urandom(32)).hexdigest()
    challenges[wallet_address] = challenge
    return challenge

class NFTMembership(db.Model):
  __tablename__ = 'nft_memberships'
  id = db.Column(db.Integer, primary_key=True) 
  contract_address = db.Column(db.String(42)) # Ethereum addresses are 42 chars 
  # Other columns like created_at etc


def verify_nft_ownership(wallet_address):
    # Construct the Alchemy API endpoint
    #endpoint = f"https://eth-mainnet.alchemyapi.io/v2/{ALCHEMY_API_KEY}"
    #endpoint = f"{ALCHEMY_API_NFT_URL}/{ALCHEMY_API_KEY}"
    endpoint = f"{ALCHEMY_API_NFT_URL}/{ALCHEMY_API_KEY}/getNFTs"
    
    # Define the payload for the request (You might need to adjust this based on the NFT contract details)
    approved_contracts = NFTMembership.query.with_entities(NFTMembership.contract_address).all()
 
    payload = {
    "owner": wallet_address,
    "contractAddresses": [contract[0] for contract in approved_contracts],
    }    
    
    response = requests.post(endpoint, json=payload)
    data = response.json()
    
    # Check if the user has the NFT (This is a basic check and might need adjustments)
    if data.get("result") and int(data["result"], 16) > 0:
        return True
    return False

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


# Initialize FileManager
config_repository = ConfigRepository() # You would define this class
file_manager = FileManager(config_repository)

@app.route('/tree', methods=['GET'])
def tree():
    disk = request.args.get('disk')
    path = request.args.get('path')
    return jsonify(file_manager.tree(disk, path))

@app.route('/upload', methods=['POST'])
def upload():
    disk = request.form['disk']
    path = request.form['path']
    files = request.files.getlist('files')
    overwrite = request.form.get('overwrite', False)
    return jsonify(file_manager.upload(disk, path, files, overwrite))

@app.route('/delete', methods=['DELETE'])
def delete():
    disk = request.form['disk']
    items = request.form['items']
    return jsonify(file_manager.delete(disk, items))

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

@app.route('/initialize', methods=['GET'])
def initialize():
    # Fetch the disk configuration from ConfigRepository
    left_disk = config_repository.get_left_disk()
    #right_disk = config_repository.get_right_disk()
    
    # Adjust the disk configuration
    disk_config = {
        'name': left_disk if left_disk else 'content',
        'path': '/storage'
    }
    
    # Construct the response structure
    response_data = {
        'result': {
            'status': 'success'
        },
        'config': {
            'disks': [disk_config],
            'settings': {
                'theme': 'light'
            }
        }
    }
    
    return jsonify(response_data)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("vue-fm/dist/" + path):
        return send_from_directory('vue-fm/dist', path)
    else:
        return send_from_directory('vue-fm/dist', 'index.html')
       
@app.route('/verify_signature', methods=['POST'])
def verify_signature():
    wallet_address = request.json.get('wallet_address')
    signature = request.json.get('signature')
    
    if not wallet_address or not signature:
        return jsonify({"error": "Wallet address and signature required"}), 400
    
    challenge = challenges.get(wallet_address)
    if not challenge:
        return jsonify({"error": "Invalid challenge"}), 400
    
    # Verify the signature using web3
    message_hash = w3.solidityKeccak(['string'], [challenge])
    recovered_address = w3.eth.account.recoverHash(message_hash, signature=signature)
    
    if recovered_address.lower() == wallet_address.lower():
        # Further check if the wallet has the NFT
        if verify_nft_ownership(wallet_address):
            return jsonify({"status": "success"})
        else:
            return jsonify({"error": "No matching NFT found in the wallet"}), 403
    else:
        return jsonify({"error": "Invalid signature"}), 403

        
@app.route('/request_challenge', methods=['POST'])
def request_challenge():
    wallet_address = request.json.get('wallet_address')
    if not wallet_address:
        return jsonify({"error": "Wallet address required"}), 400
    
    challenge = generate_challenge(wallet_address)
    return jsonify({"challenge": challenge})

if __name__ == '__main__':
    app.run(debug=True)

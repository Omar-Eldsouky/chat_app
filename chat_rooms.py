from functools import wraps
import http
import os
import threading
from bson import ObjectId
from flask import Flask, request, jsonify
# from flask_socketio import SocketIO, join_room, leave_room, emit
# from pymongo import MongoClient
import db
from flask_bcrypt import Bcrypt
import re
import phonenumbers
from email_validator import validate_email, EmailNotValidError
import secrets
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import jwt
import pytz
import asyncio
import websockets






app = Flask(__name__)

app.config['SECRET_KEY'] = '632f0470dfe889a4b83d7554a955450e'
secret_key = '632f0470dfe889a4b83d7554a955450e'

# client = MongoClient('mongodb://localhost:27017/')
# db = client['DB']
# chat_rooms = db['chat_rooms']
# private_chats = db['private_chats']
# users = db['chat_users']



UPLOAD_FOLDER = r'/home/kirito/GIT_REPO/Flask_projects/flask_chat_app/profile_pics'

active_users = set()












class User:
    def __init__(self, _id, username, email, phone):
        self._id = _id
        self.username = username
        self.email = email
        self.phone = phone


def validate_phone_number(phone_number):
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone_number, None)
        
        # Check if the parsed number is valid
        if phonenumbers.is_valid_number(parsed_number):
            return True
        else:
            return False
    except phonenumbers.phonenumberutil.NumberParseException:
        return False



def validate_password(password):
    try:
        # Check if the password meets the complexity requirements
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{9,}$', password):
            raise ValueError('Password must contain at least one uppercase letter, one lowercase letter, one number, one special character, and be at least 10 characters long!')

        # Check for repeating characters
        if re.search(r'(.)\1\1', password):
            raise ValueError('Avoid repeating characters in your password!')

        return True, None  # No error message when the password is valid

    except ValueError as error:
        return False, str(error)  # Return both the boolean value and the error message

    

def validate_email_address(email):
    try:
        # Validate the email address
        v = validate_email(email)
        return True
    except EmailNotValidError as e:
        # Email is not valid, exception message is human-readable
        return False



# def update_profile_picture(user, picture):
#     if picture:
#         # Delete the old profile picture if it exists
#         old_picture_path = os.path.join(UPLOAD_FOLDER, user['profile_pic'])
#         if os.path.exists(old_picture_path):
#             # Save the name of the old picture
#             old_picture_name = user['profile_pic']
#             # Get the number of photos for the user
#             photo_count = len([name for name in os.listdir(UPLOAD_FOLDER) if name.startswith(user['username'])])
#             # Rename the old picture with a number suffix
#             new_picture_name = f"{user['username']}_{photo_count}.jpg"
#             new_picture_path = os.path.join(UPLOAD_FOLDER, new_picture_name)
#             os.rename(old_picture_path, new_picture_path)
#             # Update the user's profile picture name in the database
#             users[user['_id']]['profile_pic'] = new_picture_name
        
#         # Save the new profile picture
#         picture_filename = secure_filename(picture.filename)
#         picture.save(os.path.join(UPLOAD_FOLDER, picture_filename))
#         # Update the user's profile picture name in the database
#         users[user['_id']]['profile_pic'] = picture_filename







# Define a function to check if the user has permission to join the chat room
# def has_permission(user_id, room_id):
    user = db.get_user_by_id(user_id)
    room = db.get_room(room_id)
    print(user)
    print(room)
    phone = user['phone']
    member = db.get_room_member(room_id, phone)
    if member:
        return True
    return False

# Define a function to authenticate users using JWT tokens
# async def authenticate(websocket):
#     token = websocket.request.query.get('token')
#     if not token:
#         return None  # No token provided

#     try:
#         data = jwt.decode(token, secret_key, algorithms=['HS256'])
#         user_id = data.get('user_id')
#         if user_id:
#             # Here, you can fetch the user from the database using the user_id if necessary
#             # For simplicity, we'll just return the user ID
#             return user_id
#     except jwt.ExpiredSignatureError:
#         return None  # Token has expired
#     except jwt.InvalidTokenError:
#         return None  # Invalid token

#     return None  # Token authentication failed for an unknown reason

# Define a decorator to require a valid token for Flask routes
def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')  # Check Authorization header
        if not token:
            # If token is not in the header, try getting it from the query parameter
            token = request.args.get('token')
        
        print("Token received:", token)  # Log the received token
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            print("Decoding token using secret key:", secret_key)  # Log the secret key
            data = jwt.decode(token.split()[1], secret_key, algorithms=['HS256'])
            print("Decoded token data:", data)  # Log the decoded token data
            kwargs['current_user_id'] = data['user_id']  # Pass user ID to the function
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            print('Invalid token')
            return jsonify({'message': 'Invalid token!'}), 403
        return f(*args, **kwargs)
    return wrapper


# # Define a function to check if the user is authorized to join the chat room
# async def is_authorized(user_id, room_id):
#     # Check if the user has permission to join the chat room
#     return has_permission(user_id, room_id)

# # Define a function to handle WebSocket connections
# async def handle_websocket(websocket, path):
#     # Perform user authentication
#     user = await authenticate(websocket)
    
#     if user:
#         # Check if the user is authorized to join the chat room
#         if await is_authorized(user, path):
#             # Proceed with WebSocket connection handling
#             await handle_chat_room(websocket, path)
#         else:
#             # If the user is not authorized, close the connection
#             await websocket.close(code=4403, reason='Unauthorized')
#     else:
#         # If authentication fails, close the connection
#         await websocket.close(code=4401, reason='Authentication Failed')

# # Define a function to handle chat room interactions
# async def handle_chat_room(websocket, room_id):
#     # Implement your chat room logic here
#     # For example, handle message sending, receiving, and broadcasting
#     pass






@app.route('/', methods=['POST'])
def home():
    return jsonify({'message': 'Welcome to chat rooms!'}), 200



@app.route('/register', methods=['GET', 'POST'])
def register():
    data = request.json
    print(data)
    username = data['username']
    email = data['email']
    phone = data['phone']
    password = data['password']
    # hashed_password = Bcrypt().generate_password_hash(password).decode('utf-8')
    query = {}
    is_valid, error_message = validate_password(password)

    if username:
        query['username'] = username
    elif email:
        query['email'] = email
    user = db.get_user(query)
    if user:
        return jsonify({'message': 'User already exists!'}), 409
    if len(username) < 3 or len(username) > 30 or ' ' in username:
        return jsonify({'message': 'Username must be between 3 and 30 characters and doesn\'t contain spaces!'}), 400

    if not is_valid:
        return jsonify({'message': error_message}), 400
    
    if not validate_phone_number(phone):
        return jsonify({'message': 'Invalid phone number!'}), 400
    
    if not validate_email_address(email):
        return jsonify({'message': 'Invalid email!'}), 400
    

    db.save_user(username, email, phone, password)
    return jsonify({'message': 'User registered successfully!'}), 201



@app.route('/login', methods=['POST'])
def login():
    local_timezone = pytz.timezone('Africa/Cairo')
    current_time = datetime.now(local_timezone)
    data = request.json
    print(data)
    phone = data['phone']
    password = data['password']
    user = db.get_user(phone)
    print(user)
    if not user:
        return jsonify({'message': 'User not found!'}), 404
    if not Bcrypt().check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid password!'}), 401
    if user and Bcrypt().check_password_hash(user['password'], password):
        token = jwt.encode({'user_id': str(user['_id']), 'exp': current_time + timedelta(days=1)}, app.config['SECRET_KEY'])
        print(current_time)
        print(current_time + timedelta(minutes=30))
        print(token)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'User logged in successfully!'}), 200



@app.route("/logout")
def logout():
    return jsonify({'message': 'User logged out successfully!'}), 200



@app.route("/account", methods=['POST', 'GET'])
@token_required
def account(current_user_id):
    if request.method == 'GET':
        user_data = db.get_user_by_id(ObjectId(current_user_id))
        if user_data:
            return jsonify({
                'username': user_data['username'],
                'email': user_data['email'],
                'phone': user_data['phone']
            }), 200
        else:
            return jsonify({'message': 'User not found!'}), 404

    elif request.method == 'POST':
        data = request.json
        username = data.get('username')
        email = data.get('email')
        phone = data.get('phone')

        if not username or not email or not phone:
            return jsonify({'message': 'Missing required data!'}), 400

        # Perform the update operations
        user_query = ObjectId(current_user_id)
        update_query = username, email, phone
        result = db.update_user(user_query, update_query)

        if result.modified_count > 0:
            return jsonify({'message': 'Account updated successfully!'}), 200
        else:
            return jsonify({'message': 'No changes made to the account!'}), 200



@app.route('/create_group', methods=['POST'])
@token_required
def create_group(current_user_id):
    data = request.json
    room_name = data['room_name']
    creator = current_user_id
    room_id = db.save_room(room_name, creator)

    if room_id:
        return jsonify({'message': 'Room created successfully!'}), 201
    else:
        return jsonify({'message': 'Failed to create room!'}), 400
    


@app.route('/rooms/<room_id>/edit', methods=['GET', 'POST'])
@token_required
def edit_room(current_user_id, room_id):
    room = db.get_room(room_id)
    print(room)

    if not room:
        return jsonify({'message': 'Room not found!'}), 404

    # Check if the current user is an admin of the room
    if not db.is_room_admin(room_id, current_user_id):
        return jsonify({'message': 'You are not authorized to edit this room!'}), 403

    if request.method == 'POST':
        # Update room details
        data = request.json
        print(data)
        new_room_name = data.get('room_name')
        
        if new_room_name:
            room['name'] = new_room_name
            db.update_room(room_id, {'name': new_room_name})

        # Handle room members update
        new_members = data.get('members', [])
        existing_members = db.get_room_members(room_id)

        members_to_add = set(new_members) - set(existing_members)
        members_to_remove = set(existing_members) - set(new_members)

        if members_to_add:
            for member in members_to_add:
                db.add_room_member(room_id, member)

        if members_to_remove:
            for member in members_to_remove:
                db.remove_room_members(room_id, member)

        return jsonify({'message': 'Room edited successfully!'}), 200

    elif request.method == 'GET':
        return jsonify({'room': room}), 200

    

@app.route('/rooms/<room_id>/messages', methods=['POST'])
@token_required
def create_message(current_user_id, room_id):
    print(current_user_id)
    phone= db.get_user_by_id(ObjectId(current_user_id))['phone']
    print(phone)
    # Verify if the user is a member of the room
    if not db.is_room_member(room_id, phone):
        return jsonify({'message': 'You are not authorized to send messages in this room!'}), 403

    # Retrieve the message data from the request
    data = request.json
    print(data)
    sender = phone
    message_content = data.get('content')

    # Save the message to the database
    db.save_message(room_id, sender, message_content)

    return jsonify({'message': 'Message sent successfully!'}), 201
    
    


@app.route('/rooms/<room_id>/')
@token_required
def view_room(current_user_id, room_id):
    room = db.get_room(room_id)
    if room and db.is_room_member(room_id, current_user_id):
        room_members = db.get_room_members(room_id)
        message= db.get_message(room_id)
        return jsonify({'room': room, 'room_members': room_members,'messsage': message}), 200
    else:
        return jsonify({'message': 'Room not found!'}), 404




@app.route('/chat/<room_id>')
async def chat_room(websocket, room_id):
    # Handle WebSocket connections
    while True:
        message = await websocket.recv()
        print(f"Message received: {message}")
        db.save_message(room_id, message)
        
        await websocket.send(message)  # Send the message back to the client









async def send_message(websocket, message):
    await websocket.send(message)
    response = await websocket.recv()
    print(response)







# async def start_websocket_server():
#     await websockets.serve(chat_room, '127.0.0.2', 8767)


async def start_websocket_server():
    server = await websockets.serve(chat_room, '127.0.0.1', 8766)
    await server.wait_closed()

def start_servers():
    # Start the Flask server
    app.run(debug=True, port=5000, host='127.0.0.1', use_reloader=False)

    # Start the WebSocket server
    asyncio.run(start_websocket_server())

if __name__ == '__main__':
    # Create a thread for running both servers
    server_thread = threading.Thread(target=start_servers)

    # Start the thread
    server_thread.start()

    # Wait for the thread to finish
    server_thread.join()
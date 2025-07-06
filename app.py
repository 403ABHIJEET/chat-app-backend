from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, emit
import os

app = Flask(__name__)
CORS(app, origins="*")
socketio = SocketIO(app, cors_allowed_origins="*")

# Track users' socket IDs
connected_users = {}

@app.route('/')
def index():
    return "Flask Chat Server is running"

@socketio.on('connect')
def handle_connect():
    print("A user connected")

@socketio.on('register')
def register_user(data):
    user_id = data.get('user_id')
    if user_id:
        connected_users[user_id] = request.sid
        join_room(user_id)
        print(f"User {user_id} joined their room.")

@socketio.on('private_message')
def handle_private_message(data):
    sender = data['sender_id']
    recipient = data['recipient_id']
    message = data['message']
    
    print(f"{sender} to {recipient}: {message}")

    # Emit to recipient's room
    emit('new_message', {
        'sender': sender,
        'message': message
    }, room=recipient)

@socketio.on('disconnect')
def handle_disconnect():
    print(f"User disconnected: {request.sid}")
    # Optional: remove from connected_users

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

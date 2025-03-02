from ollama import chat
from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def serve_index():
    return send_from_directory('.', 'client.html')

@socketio.on('connect')
def handle_connect():
    client_id = request.sid
    print(f'Client connected: {client_id}')


@socketio.on('message')
def handle_message(data):
    user_message = data['message']
    stream = chat(
        # model='deepseek-r1:1.5b',
        model='llama3',
        messages=[{'role': 'user', 'content': user_message}],
        stream=True,
    )
    random_id = str(uuid.uuid4())
    for chunk in stream:
        emit('response', {'message': chunk['message']['content'], 'id': random_id}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
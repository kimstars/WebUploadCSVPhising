from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('process_item')
def process_item(item):
    # Xử lý item và gửi kết quả về client
    result = 'Processed: ' + item
    socketio.emit('result', result)

if __name__ == '__main__':
    socketio.run(app)

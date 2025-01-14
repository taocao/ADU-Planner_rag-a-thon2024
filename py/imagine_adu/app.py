from dotenv import load_dotenv

from flask import Flask
from flask_socketio import SocketIO, emit

load_dotenv()

from agent.agent import query
from layout.query import find_layouts

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on("message")
def handle_json(json):
    def callback(msg, event="info"):
        emit(event, msg)
        print(msg)

    address = json["address"]
    callback("Agent: finding local building codes...")
    build_code = query(address, callback)
    callback(f"Internal: found, {str(build_code)}")
    for layout in find_layouts(address, build_code, callback):
        callback(layout, event="layout")


if __name__ == "__main__":
    socketio.run(app)

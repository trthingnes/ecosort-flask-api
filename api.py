from dotenv import load_dotenv

load_dotenv()

from flask import Flask, request, Response, jsonify
from chat import create_conversation, send_message_in_conversation
from object_recognition import recognize_objects_from_image

app = Flask(__name__)


@app.route("/")
def root():
    return jsonify({"status": "running"})


@app.route("/chats", methods=["POST"])
def start_chat():
    body = request.get_json()
    message = body.get("message", None)
    c_id, messages = create_conversation()

    return jsonify({"id": c_id, "messages": [dict(m) for m in messages[1:]]})


@app.route("/chats/<id>", methods=["POST"])
def continue_chat(id):
    body = request.get_json()
    message = body.get("message", None)
    c_id, messages = send_message_in_conversation(id, message)

    return jsonify({"id": c_id, "messages": [dict(m) for m in messages[1:]]})


@app.route("/image", methods=["POST"])
def image_recognition():
    return jsonify(recognize_objects_from_image(request.data))


# Start the Flask API when file is executed
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

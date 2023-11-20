from flask import Flask, request, jsonify
from chat import forward_message_to_openai
from object_recognition import recognize_objects_from_image

app = Flask(__name__)

# Flask API main endpoint
@app.route("/")
def root():
    return jsonify({ "status": "running" })

@app.route("/chat", methods=["POST"])
def chat_message():
    body = request.get_json()
    conversation_id = body.get("conversation_id", None)
    message = body.get("message", None)

    return jsonify(forward_message_to_openai(conversation_id, message))

@app.route("/image", methods=["POST"])
def image_recognition():
    return jsonify(recognize_objects_from_image(request.data))

# Start the Flask API when file is executed
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
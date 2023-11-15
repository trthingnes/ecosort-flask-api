from flask import Flask, jsonify
from waitress import serve

# Define constants and Flask application
app = Flask(__name__)

# Define Flask appliation endpoints
@app.route("/")
def root():
    return jsonify({ "status": "running" })

#@app.route("/image")
#def recognize_object_from_image():

# Run the Flask API based on the configuration above
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
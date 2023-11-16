from flask import Flask, request, jsonify
from waitress import serve

app = Flask(__name__)

# Flask API main endpoint
@app.route("/")
def root():
    return jsonify({ "status": "running" })

# Object recognition from image
import torch
from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image
from io import BytesIO

number_of_predictions = 5
model_name = 'google/vit-base-patch16-224'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = ViTForImageClassification.from_pretrained(model_name)
model.to(device)
processor = ViTImageProcessor.from_pretrained(model_name)

@app.route("/image", methods=["POST"])
def recognize_objects_from_image():
    image_blob = request.data
    image = Image.open(BytesIO(image_blob))
    inputs = processor(images=image, return_tensors="pt").to(device)
    pixel_values = inputs.pixel_values

    with torch.no_grad():
        outputs = model(pixel_values)
    logits = outputs.logits
    values, indices = torch.topk(logits, number_of_predictions)
    
    scores = []
    for v, i in zip(values.flatten(), indices.flatten()):
        scores.append({ "score": round(v.item(), 2), "label": model.config.id2label[i.item()] })

    return jsonify({ "scores": scores })

# Start the Flask API when file is executed
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
    # serve(app, host="0.0.0.0", port=8080)
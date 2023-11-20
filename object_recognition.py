import torch
from PIL import Image
from io import BytesIO
from transformers import ViTForImageClassification, ViTImageProcessor

number_of_predictions = 5
model_name = 'google/vit-base-patch16-224'
processor = ViTImageProcessor.from_pretrained(model_name)
model = ViTForImageClassification.from_pretrained(model_name)

def recognize_objects_from_image(image_blob):
    image = Image.open(BytesIO(image_blob))
    inputs = processor(images=image, return_tensors="pt")
    pixel_values = inputs.pixel_values

    with torch.no_grad():
        outputs = model(pixel_values)
    logits = outputs.logits
    values, indices = torch.topk(logits, number_of_predictions)
    
    scores = []
    for v, i in zip(values.flatten(), indices.flatten()):
        scores.append({ "score": round(v.item(), 2), "label": model.config.id2label[i.item()] })

    return scores
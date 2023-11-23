import torch
from PIL import Image
from io import BytesIO
from transformers import ViTForImageClassification, ViTImageProcessor

MODEL = "google/vit-base-patch16-224"
N_PREDICTIONS = 5

processor = ViTImageProcessor.from_pretrained(MODEL)
model = ViTForImageClassification.from_pretrained(MODEL)


def recognize_objects_from_image(image_blob):
    image = Image.open(BytesIO(image_blob))
    inputs = processor(images=image, return_tensors="pt")
    pixel_values = inputs.pixel_values

    with torch.no_grad():
        outputs = model(pixel_values)
    logits = outputs.logits
    values, indices = torch.topk(logits, N_PREDICTIONS)

    scores = []
    for v, i in zip(values.flatten(), indices.flatten()):
        scores.append(
            {"score": round(v.item(), 2), "label": model.config.id2label[i.item()]}
        )

    return scores

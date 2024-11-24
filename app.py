from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import io
import base64
import cv2
import numpy as np
import tensorflow as tf


# Initialize app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sssse'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Photo(db.Model):
    __tablename__ = 'dailyphoto'
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.Text, nullable=False)  # Base64 image
    description = db.Column(db.String(255), nullable=True)
    postdate = db.Column(db.DateTime, nullable=False)
    items = db.Column(db.Text, nullable=True)  # Detected items

# Helper function: Decode base64 to OpenCV Image
def decode_base64_image(base64_string):
    img_data = base64.b64decode(base64_string)
    img_array = np.frombuffer(img_data, np.uint8)
    return cv2.imdecode(img_array, cv2.IMREAD_COLOR)

def load_labels(filepath):
    with open(filepath, 'r') as f:
        labels = f.read().strip().split("\n")
    return labels



# Object detection using OpenCV
def detect_objects(img):
    # Load the TFLite model from the local directory
    model = tf.saved_model.load('./models/ssd_mobilenet_v2/saved_model')
    LABELS = load_labels('./models/coco_labels.txt')
    # Get the inference function
    detect_fn = model.signatures['serving_default']

    # Preprocess the image: Resize and convert to uint8
    input_tensor = cv2.resize(img, (300, 300))  # Resize to model input size
    input_tensor = tf.convert_to_tensor(input_tensor, dtype=tf.uint8)  # Convert to uint8
    input_tensor = tf.expand_dims(input_tensor, axis=0)  # Add batch dimension

    # Perform inference
    detections = detect_fn(input_tensor)

    # Extract bounding boxes, class IDs, and confidence scores
    boxes = detections['detection_boxes'].numpy()[0]  # Bounding boxes
    scores = detections['detection_scores'].numpy()[0]  # Confidence scores
    classes = detections['detection_classes'].numpy()[0].astype(int)  # Class IDs

    # Apply NMS
    nms_indices = tf.image.non_max_suppression(
        boxes=boxes,
        scores=scores,
        max_output_size=10,  # Maximum number of objects to detect
        iou_threshold=0.5,  # Overlap threshold for suppression
        score_threshold=0.5  # Confidence score threshold
    ).numpy()

    # Filter results based on NMS indices
    detected_items = [LABELS[classes[i] - 1] for i in nms_indices]  # Map class IDs to labels

    return detected_items

@app.route('/')
def index():
    # Fetch all photos and sort by postdate
    print("test")
    photos = Photo.query.order_by(Photo.postdate.desc()).all()
    print("run")
    for photo in photos:
        if not photo.items:
            img = decode_base64_image(photo.photo)
            detected_items = detect_objects(img)
            photo.items = ', '.join(detected_items)
            db.session.commit()  # Save detected items to database
    return render_template('index.html', photos=photos)

@app.route('/detect', methods=['POST'])
def detect():
    print("Run all detection")
    photos = Photo.query.all()
    for photo in photos:
        img = decode_base64_image(photo.photo)
        detected_items = detect_objects(img)
        photo.items = ', '.join(detected_items)
        db.session.commit()  # Save detected items to database
    return "Detection complete. Refresh the homepage!"

# Run server
if __name__ == "__main__":
    app.run(debug=True, port=5100)

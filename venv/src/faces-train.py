import os
import numpy as np
import cv2
import pickle
from PIL import Image

frontal_face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')

# Open image directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "images")

current_id = 0
# Create empty dictionary
label_ids = {}
# Stores folder names (labels)
y_labels = []
# Stores images as array
x_train = []

# Create recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Iterates through images folder
for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg") or file.endswith("PNG") or file.endswith("JPG"):
            # Gets absolute path of image
            path = os.path.join(root, file)

            # Create label from folder name
            label = os.path.basename(root).replace(" ", "-").lower()

            print(label)

            # Assign each folder a label id
            if label not in label_ids:
                label_ids[label] = current_id
                current_id += 1
            id_ = label_ids[label]

            # Gets image using Plllow library (Python Image Library)
            pil_image = Image.open(path).convert("L") # Converts to grayscale

            # Converts image to number array
            image_array = np.array(pil_image, "uint8")

            faces = frontal_face_cascade.detectMultiScale(image_array)

            # Added detected faces to train list
            for (x, y, w, h) in faces:
                roi = image_array[y:y+h, x:x+w]
                x_train.append(roi)
                y_labels.append(id_)

# Using pickle library, writes label ids to file
with open("labels.pickle", 'wb') as f:
    pickle.dump(label_ids, f)

# Start recognizer training
recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainer.yml")
import tensorflow as tf
import numpy as np

# Load the saved model
pb_model_dir = "inference_graph/saved_model"
model = tf.saved_model.load(pb_model_dir)
category_index = {1: {'id': 1, 'name': 'Barath'},
                  2: {'id': 2, 'name': 'Gokul'},
                  3: {'id': 3, 'name': 'Kishore'},
                  4: {'id': 4, 'name': 'Rajakumaran'},
                  5: {'id': 5, 'name': 'Vasant'}}


def format_image(image):
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = tf.expand_dims(image, axis=0)
    image = tf.image.resize(image, [224, 224])
    image = tf.cast(image, tf.uint8)
    print("Image Formatting Successful")
    return image


def predict(image):
    image = format_image(image)
    detections = model(image)
    threshold = 0.5  # Set the threshold for detection confidence
    detected_names = []
    for i in range(len(detections['detection_scores'][0])):
        score = detections['detection_scores'][0][i]
        if score >= threshold:
            class_id = int(detections['detection_classes'][0][i])
            class_name = category_index[class_id]['name']
            detected_names.append(class_name)
    output = {'detected_names': detected_names}
    print("Possibilities--{}".format(output))
    if output['detected_names']:
        return output['detected_names'][0]
    else:
        return "None"

import os
import shutil
import logging
import numpy as np
from PIL import Image
import tensorflow as tf

from quicklearning.classification.image import disable_tensorflow_warnings

class Lite(object):
    @disable_tensorflow_warnings
    def __init__(self, model, image_size, classes=[]):
        self.classes = classes
        self.image_size = image_size

        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        self.model = converter.convert()

        self.interpreter = tf.lite.Interpreter(model_content=self.model)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def save(self, folder="."):
        self._create_folder(folder)
        with open("{}/model.tflite".format(folder), "wb") as file:
            file.write(self.model)
        with open("{}/labels.txt".format(folder),'w') as file:
            file.write("\n".join(self.classes))

    def predict(self, file):
        input_img = Image.open(file).convert('RGB')
        input_img = input_img.resize((self.image_size, self.image_size))
        input_img = np.expand_dims(input_img, axis=0)
        input_img = (np.float32(input_img) - 0.) / 255.
        
        self.interpreter.set_tensor(self.input_details[0]['index'], input_img)
        self.interpreter.invoke()
        prediction = self.interpreter.get_tensor(self.output_details[0]['index'])
        index = np.argmax(prediction)

        return self.classes[index], prediction[0][index]

    def _create_folder(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

    def _remove_folder(self, folder):
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)

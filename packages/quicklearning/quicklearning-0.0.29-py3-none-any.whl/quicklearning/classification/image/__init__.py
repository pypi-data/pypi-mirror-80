import io
import os
import shutil
import logging
from PIL import Image
import matplotlib.pyplot as plt

import tensorflow as tf
import tensorflow_hub as hub

from model import Model
from lite import Lite

def disable_tensorflow_warnings(func):
    def inner(*args, **kwargs):
        logging.getLogger("tensorflow").setLevel(logging.ERROR)
        x = func(*args, **kwargs)
        logging.getLogger("tensorflow").setLevel(logging.WARNING)
        return x
    return inner

def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def remove_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder, ignore_errors=True)

def list_files(path):
    return [name for name in os.listdir(path) if os.path.isfile("{}/{}".format(path, name))]

def list_folders(path):
    return [name for name in os.listdir(path) if os.path.isdir("{}/{}".format(path, name))]

def plot(title, xlabel, ylabel, series=[], leyend=[]):
    for serie in series:
        plt.plot(serie)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.legend(leyend, loc='upper left')

    buf = io.BytesIO()
    plt.savefig(buf)
    plt.close()
    buf.seek(0)
    return Image.open(buf)

def load_h5_model(model_file="model.h5", labels_file='labels.tf'):
    loaded_model = tf.keras.models.load_model(model_file, custom_objects={'KerasLayer':hub.KerasLayer})

    labels_file = open(labels_file, 'r')
    classes = [c.strip() for c in labels_file.readlines()]

    return Model(loaded_model, classes=classes)

def load_tf_model(model_folder="model.tf", labels_file='labels.tf'):
    loaded_model = tf.keras.models.load_model(model_folder)

    labels_file = open(labels_file, 'r')
    classes = [c.strip() for c in labels_file.readlines()]

    return Model(loaded_model, classes=classes)

def load_tf_lite_model(model_file="model.tflite", labels_file="labels.tf"):
    model_file = open(model_file, "rb")
    loaded_model = model_file.read()

    labels_file = open(labels_file, 'r')
    classes = [c.strip() for c in labels_file.readlines()]

    return Lite(loaded_model, classes=classes, is_tf_lite_model=True)
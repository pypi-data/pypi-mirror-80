import os
import shutil
import DuckDuckGoImages as ddg
import tensorflow_hub as hub
from tensorflow.nn import softmax
from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import optimizers
from tensorflow.keras import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator

#self, classification_name, images_path, models_base_dir, logs_base_dir
#self, model=None, image_size=None, optimizer=None, epochs=10000, batch_size=32, split=0.2, verbose=False

balanced = (
    hub.KerasLayer("https://tfhub.dev/google/efficientnet/b0/feature-vector/1", trainable=False),
    224,
    optimizers.RMSprop(learning_rate=0.001)
)

def fit(input_model, epochs, classes=[], data_folder="./images", batch_size=32, split=0.2, verbose=False):
    (transfer_learning_layer, size, optimizer) = input_model

    _download_data(data_folder, classes)
    train, validation = _create_image_data_generator(data_folder, size, batch_size, split)
    model = _create_model(transfer_learning_layer, size, optimizer, classes)
    
    steps_per_epoch = train.n//train.batch_size
    validation_steps = validation.n//validation.batch_size

    model.fit(
        train,
        epochs=epochs,
        validation_data=validation,
        steps_per_epoch=steps_per_epoch,
        validation_steps=validation_steps,
        verbose=verbose
    )
    return model

def _download_data(data_folder, classes):
    _create_folder(data_folder)
    for item in classes:
        if not os.path.exists('{}/{}'.format(data_folder, item)):
            ddg.download(item, folder='{}/{}'.format(data_folder, item), thumbnails=True, parallel=True)

def _create_model(transfer_learning_layer, size, optimizer, classes):
    model = Sequential([
        transfer_learning_layer,
        layers.Dense(len(classes), activation=softmax)
    ])
    if len(classes) <= 2:
        loss = losses.BinaryCrossentropy(from_logits=True)
    else:
        loss = losses.CategoricalCrossentropy(from_logits=True)

    model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])
    model.build([None, size, size, 3])
    return model

def _create_image_data_generator(data_folder, image_size, batch_size, validation_split):
        generator = ImageDataGenerator(
            rescale=1/255,
            validation_split=validation_split,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True
        )
        train_data = generator.flow_from_directory(
            data_folder, target_size=(image_size, image_size), subset='training', batch_size=batch_size
        )
        validation_data = generator.flow_from_directory(
            data_folder, target_size=(image_size, image_size), subset='validation', batch_size=batch_size
        )
        return train_data, validation_data

def _create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def _remove_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder, ignore_errors=True)
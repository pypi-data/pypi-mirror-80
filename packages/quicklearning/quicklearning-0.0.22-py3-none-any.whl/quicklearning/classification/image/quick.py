import os
import DuckDuckGoImages as ddg
from tqdm.auto import tqdm
from joblib import Parallel, delayed

import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import optimizers
from tensorflow.keras import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from quicklearning.classification.image import list_files
from quicklearning.classification.image.model import Model
from quicklearning.classification.image import create_folder
from quicklearning.classification.image import remove_folder
from quicklearning.classification.image.callbacks import EarlyStop, LearningRateReducer

mobilenet_v2 = (hub.KerasLayer("https://tfhub.dev/google/imagenet/mobilenet_v2_100_96/feature_vector/4", trainable=False), 96)
efficientnet_b0 = (hub.KerasLayer("https://tfhub.dev/google/efficientnet/b0/feature-vector/1", trainable=False), 224)
inception_v3 = (hub.KerasLayer("https://tfhub.dev/google/imagenet/inception_v3/feature_vector/4", trainable=False), 299)
efficientnet_b7 = (hub.KerasLayer("https://tfhub.dev/google/efficientnet/b7/feature-vector/1", trainable=False), 600)

def fit(epochs, input_model=efficientnet_b0, optimizer=optimizers.RMSprop(), classes=[], data_folder="./images", batch_size=32, validation_split=0.2, predict_retrain_loops=0, verbose=False):
    (transfer_learning_layer, size) = input_model

    _download_data(data_folder, classes)
    
    model = Model(
        _create_model(transfer_learning_layer, size, optimizer, classes),
        size,
        data_folder=data_folder,
        batch_size=batch_size,
        validation_split=validation_split,
        callbacks=[
            EarlyStop(),
            LearningRateReducer()
        ],
        verbose=verbose
    )
    model.fit(epochs)

    for _ in range(predict_retrain_loops):
        bad_predictions = remove_bad_prediction_files(model, data_folder)
        if bad_predictions > 0:
            model = Model(
                _create_model(transfer_learning_layer, size, optimizer, classes),
                size,
                data_folder=data_folder,
                batch_size=batch_size,
                validation_split=validation_split,
                callbacks=[
                    EarlyStop(),
                    LearningRateReducer()
                ],
                verbose=verbose
            )
            model.fit(epochs)
        else:
            return model
    return model

def remove_bad_prediction_files(model, data_folder):
    removed_files = 0
    with tqdm(model.classes, desc='refine', unit="class") as bar:
        for c in bar:
            files = list_files('{}/{}'.format(data_folder, c))
            for file in tqdm(files, desc='refining class {}'.format(c), unit="img", leave=False):
                prediction, _ = model.predict(file='{}/{}/{}'.format(data_folder, c, file))
                if prediction is not c:
                    os.remove('{}/{}/{}'.format(data_folder, c, file))
                    removed_files += 1
                    bar.set_postfix(removed_files=removed_files)
    return removed_files

def _download_data(data_folder, classes):
    remove_folder(data_folder)
    create_folder(data_folder)
    with tqdm(classes, desc="downloading dataset", unit="class") as bar:
        for item in bar:
            if not os.path.exists('{}/{}'.format(data_folder, item)):
                folder='{}/{}'.format(data_folder, item)
                urls = ddg.get_image_thumbnails_urls(item)
                downloaded = 0
                with Parallel(n_jobs=os.cpu_count()) as parallel:
                    results = parallel(delayed(ddg._download)(url, folder) for url in tqdm(urls, desc=item, unit="img", leave=False))
                    for result in results:
                        if result:
                            downloaded += 1
                            bar.set_postfix(total_downloads=downloaded)

def _create_model(transfer_learning_layer, size, optimizer, classes):
    model = Sequential([
        transfer_learning_layer,
        layers.Dense(len(classes), activation=tf.nn.softmax)
    ])
    if len(classes) <= 2:
        loss = losses.BinaryCrossentropy(from_logits=True)
    else:
        loss = losses.CategoricalCrossentropy(from_logits=True)

    model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])
    model.build([None, size, size, 3])
    return model
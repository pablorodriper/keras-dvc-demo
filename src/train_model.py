import json
import os

import dvc.api
import matplotlib.pyplot as plt
from mlem.api import save
from tensorflow.keras import Sequential
from tensorflow.keras.applications import EfficientNetV2B0 as EfficientNet
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import SGD

from utils import load_dataset


def define_model(params):
    """
    Define model architecture
    """
    
    image_size = tuple(params["model"]["image_size"])

    model = Sequential()
    model.add(EfficientNet(include_top=False, 
                           weights='imagenet', 
                           input_shape=(*image_size,3)))
    model.add(Flatten())
    model.add(Dense(50, activation='softmax', name="output_layer"))

    model.compile(optimizer=SGD(learning_rate=params["train"]["learning_rate"]),   # https://www.tensorflow.org/api_docs/python/tf/keras/optimizers
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model


def train_model(params, model, train_data, val_data):
    """
    Train model
    """
    history = model.fit(train_data, 
                        epochs=params["train"]["epochs"], # 2, 
                        validation_data=val_data) 
                        # class_weight={0: 0.7, 1: 0.3})

    return history


def save_metrics(params, history):
    """
    Save DVC metrics to disk
    """
    with open(params["train"]["metrics_path"], 'w') as outfile:
        json.dump({"accuracy": history.history['accuracy'][-1],
                   "val_accuracy": history.history['val_accuracy'][-1]}, 
                  outfile)


def save_plots(params, history):
    """
    Save accuracy and loss plots to disk
    """
    if not os.path.exists(params["common"]["plots_path"]):
        os.makedirs(params["common"]["plots_path"])

    # Accuracy
    plt.figure(0)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.ylim(0.8, 1.02)
    plt.grid(axis='y', color='0.95')
    plt.legend(['train', 'val'], loc='upper left')
    plt.savefig(params["train"]["accuracy_plot_path"])

    # Loss
    plt.figure(1)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.ylim(0, 0.4)
    plt.grid(axis='y', color='0.95')
    plt.legend(['train', 'val'], loc='upper left')
    plt.savefig(params["train"]["loss_plot_path"])


def save_model(params, model):
    """
    Save model to disk in .pb format
    """
    # Save model with MLEM
    save(model, "model")

    # Save model to models folder, where it can be used by tf2onnx
    model.save(params["model"]["model_pb_path"])


if __name__ == "__main__":
    params = dvc.api.params_show(stages="train")
    
    train_data = load_dataset(params, "train") 
    val_data = load_dataset(params, "eval")

    model = define_model(params)
    history = train_model(params, model, train_data, val_data)
    save_metrics(params, history)
    save_plots(params, history)
    save_model(params, model)

import dvc.api
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.applications import EfficientNetV2B0 as EfficientNet

def load_datasets(params):
    seed=params["common"]["seed"]

    # Create data generator from folder
    image_size = tuple(params["train"]["image_size"])

    train_data = image_dataset_from_directory(
        directory=params["train"]["data_path"],
        labels='inferred',
        label_mode='categorical',
        color_mode='rgb',
        batch_size=params["train"]["batch_size"],
        image_size=image_size, # https://github.com/sebastian-sz/efficientnet-v2-keras#input-shapes
        #crop_to_aspect_ratio=True,
        seed=seed)

    val_data = image_dataset_from_directory(
        directory=params["eval"]["data_path"],
        labels='inferred',
        label_mode='categorical',
        color_mode='rgb',
        batch_size=params["train"]["batch_size"],
        image_size=image_size,
        seed=seed)

    return train_data, val_data


def define_model(params):
    
    image_size = tuple(params["train"]["image_size"])

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
    history = model.fit(train_data, 
                        epochs=params["train"]["epochs"], # 2, 
                        validation_data=val_data) 
                        # class_weight={0: 0.7, 1: 0.3})

    return history


def save_model(params, model):
    model.save(params["train"]["model_pb_path"])

if __name__ == "__main__":
    params = dvc.api.params_show(stages="train")
    
    train_data, val_data = load_datasets(params) # TODO: Change to call two times load_dataset(params, dataset_name)
    model = define_model(params)
    history = train_model(params, model, train_data, val_data)
    save_model(params, model)

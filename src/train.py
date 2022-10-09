import dvc.api
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.applications import EfficientNetV2B0 as EfficientNet


def load_dataset(params, dataset_name):
    """
    Load dataset from folder using DVC params

    Args:
        params (dict): DVC params
        dataset_name (str): name of the dataset to load

    Returns:
        dataset: data generator
    """
    seed=params["common"]["seed"]

    # Create data generator from folder
    dataset = image_dataset_from_directory(
        directory=params[dataset_name]["data_path"],
        labels='inferred',
        label_mode='categorical',
        color_mode='rgb',
        batch_size=params["train"]["batch_size"],
        image_size=tuple(params["train"]["image_size"]), # https://github.com/sebastian-sz/efficientnet-v2-keras#input-shapes
        #crop_to_aspect_ratio=True,
        seed=seed)

    return dataset


def define_model(params):
    """
    Define model architecture
    """
    
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
    """
    Train model
    """
    history = model.fit(train_data, 
                        epochs=params["train"]["epochs"], # 2, 
                        validation_data=val_data) 
                        # class_weight={0: 0.7, 1: 0.3})

    return history


def save_model(params, model):
    """
    Save model to disk in .pb format
    """
    model.save(params["train"]["model_pb_path"])


if __name__ == "__main__":
    params = dvc.api.params_show(stages="train")
    
    train_data = load_dataset(params, "train") 
    val_data = load_dataset(params, "eval")

    model = define_model(params)
    history = train_model(params, model, train_data, val_data)
    save_model(params, model)

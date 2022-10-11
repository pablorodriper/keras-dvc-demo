from tensorflow.keras.models import load_model
from tensorflow.keras.utils import image_dataset_from_directory


def load_dataset(params, dataset_name, shuffle=True):
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
        shuffle=shuffle,
        color_mode='rgb',
        batch_size=params["model"]["batch_size"],
        image_size=tuple(params["model"]["image_size"]), # https://github.com/sebastian-sz/efficientnet-v2-keras#input-shapes
        #crop_to_aspect_ratio=True,
        seed=seed)

    return dataset


def load_pb_model(params):
    return load_model(params["model"]["model_pb_path"])
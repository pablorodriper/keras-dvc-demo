import json
import os
from glob import glob

import dvc.api
from splitfolders import ratio


def split_data(params, input_data_folder):
    """
    Split data into train and validation
    """
    ratio(input_data_folder, 
          params["split"]["split_data_path"], 
          ratio=(params["split"]["train_split"], 
                 params["split"]["validation_split"], 
                 params["split"]["test_split"]), 
          seed=params["common"]["seed"])


def save_metrics(params):
    """
    Save DVC metrics to disk
    """
    metrics = {
        "train size": sum([len(files) for r, d, files in os.walk(params["train"]["data_path"])]),
        "val size":  sum([len(files) for r, d, files in os.walk(params["eval"]["data_path"])]),
        "test size":  sum([len(files) for r, d, files in os.walk(params["test"]["data_path"])])
    }
    print(metrics)

    with open(params["split"]["metrics_path"], 'w') as outfile:
        json.dump(metrics, outfile)


if __name__ == "__main__":
    params = dvc.api.params_show(stages="make_dataset")

    # Create train and validation datasets
    for input_data_folder in glob(params["split"]["raw_data_path"]+"*/"):
        print(input_data_folder)
        split_data(params, input_data_folder)

    save_metrics(params)

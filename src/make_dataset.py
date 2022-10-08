from glob import glob

import dvc.api
from splitfolders import ratio


def split_data(params, input_data_folder):
    """
    Split data into train and validation sets
    """
    # Split data into train and validation folders
    ratio(input_data_folder, 
          params["common"]["split_data_path"], 
          ratio=(params["split"]["train_split"], 
                 params["split"]["validation_split"]), 
          seed=params["common"]["seed"])

if __name__ == "__main__":
    params = dvc.api.params_show(stages="make_dataset")

    # Create train and validation dataset
    for input_data_folder in glob(params["common"]["raw_data_path"]+"*/"):
        print(input_data_folder)
        split_data(params, input_data_folder)

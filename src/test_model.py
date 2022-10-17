import json

import dvc.api
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, confusion_matrix

from utils import load_dataset, load_pb_model


def evaluate_model(params, model, dataset_name, data_not_shuffle):

    y_true = np.argmax(np.concatenate([y for x, y in data_not_shuffle], axis=0), axis=1)
    print(y_true)

    Y_pred = model.predict(data_not_shuffle)
    y_pred = np.argmax(Y_pred, axis=1)
    print(y_pred)

    # Classification report
    print(classification_report(y_true, y_pred))
    classif_report_dict = classification_report(y_true, y_pred, output_dict=True)
    with open(params[dataset_name]["metrics_path"], 'w') as outfile:
        json.dump(classif_report_dict, outfile) 

    # Confusion matrix
    print(confusion_matrix(y_true, y_pred))

    ConfusionMatrixDisplay.from_predictions(y_true, y_pred, 
                                            normalize="true", 
                                            include_values=False,
                                            cmap='Blues')
    plt.title("Confusion Matrix")
    plt.xlabel("Pred")
    plt.ylabel("True")

    plt.savefig(params[dataset_name]["confusion_matrix_path"])


if __name__ == "__main__":
    params = dvc.api.params_show(stages="test")
    print(params)
    dataset_name = "test"
    
    validation_data_not_shuffle = load_dataset(params, 
                                               dataset_name, 
                                               shuffle=False)
    
    model = load_pb_model(params)
    evaluate_model(params, model, dataset_name, validation_data_not_shuffle)
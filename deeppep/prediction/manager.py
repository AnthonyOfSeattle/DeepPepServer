import os
import tensorflow as tf
from tensorflow.keras import models, backend

tf.get_logger().setLevel('ERROR')

class PredictionManager:
    def __init__(self, model_name, config_path, weight_path):
        self.model_name = model_name
        self.config_path = self._check_path(config_path)
        self.weight_path = self._check_path(weight_path)
        self.model = self._load_model()

    def __del__(self):
        backend.clear_session()

    def _path_not_found_message(self, path):
        message = " ".join([
            "MODEL LOADING ERROR:",
            "Could not find file for model {},"
            "at the path: {}"
            ]).format(self.model_name, path)

        return message

    def _check_path(self, path):
        if not os.path.exists(path):
            raise HTTPException(status_code=500,
                                detail = self._path_not_found_message(path)
                                )
        return path

    def _model_not_loaded_message(self):
        message = " ".join([
            "MODEL LOADING ERROR:",
            "Could not load model {}."
            ]).format(self.model_name)

        return message


    def _load_model(self):
        try:
            with open(self.config_path, "r") as config:
                model = models.model_from_json(config.read())
            model.load_weights(self.weight_path)

            return model

        except:
            raise HTTPException(status_code=500,
                                detail=self._model_not_loaded_message())

    def predict(self, input):
        output = self.model.predict(input)
        return output

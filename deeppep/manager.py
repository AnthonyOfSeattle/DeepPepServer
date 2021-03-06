from fastapi import HTTPException
from .types import Action, PreprocessingConfig, merge_configs
from .config import get_model_info
from .preprocessing import PreprocessingManager
from .prediction import PredictionManager

class PipelineManager:
    def __init__(self, model_name, user_config=None):
        self.model_name = model_name
        self.model_config = self._get_model_config(self.model_name)
        self.pre_config = PreprocessingConfig()
        self.pre_config = merge_configs(self.pre_config,
                                        self.model_config.pre_config
                                       )
        if user_config is not None:
           self.pre_config = merge_configs(self.pre_config,
                                           user_config
                                           ) 

    def _model_missing_message(self, model_name):
        message = " ".join([
            "Model Not Found:",
            "The model, {}, could not be found.",
            "Please send an OPTIONS request to the following address",
            "in order to get a list of available models: /models"
            ]).format(model_name)

        return message

    def _get_model_config(self, model_name):
        model_info = get_model_info()
        if not model_name in model_info:
            raise HTTPException(status_code = 404,
                                detail = self._model_missing_message(model_name)
                                )

        return model_info[model_name]

    def _check_encoding_permission(self):
        if not self.model_config.allow_encoding:
            raise HTTPException(status_code = 404,
                                detail = "Resource's encodings are not available")

    def _preprocess_peptides(self, peptides):
        pre_manager = PreprocessingManager(**self.pre_config.dict())
        peptides = pre_manager.preprocess(
            [pep.sequence for pep in peptides]
        )

        return peptides

    def _predict(self, enc_peptides):
        pred_manager = PredictionManager(model_name=self.model_name,
                                         config_path=self.model_config.config_path,
                                         weight_path=self.model_config.weight_path)

        predictions = pred_manager.predict(enc_peptides)
        return predictions

    def _encode(self, enc_peptides):
        pred_manager = PredictionManager(model_name=self.model_name,
                                         config_path=self.model_config.config_path,
                                         weight_path=self.model_config.weight_path)

        encodings = pred_manager.encode(enc_peptides)
        return encodings

    def _build_output(self, peptides, predictions, output_labels=None):
        if output_labels is None:
            output = [{"values" : pred} for pred in predictions.tolist()]

        else:
            output = []
            for pred_set in predictions:
                output.append(
                    {label : pred for label, pred in zip(output_labels, pred_set.tolist())}
                    )

        [item.update(pep.dict()) for pep, item in zip(peptides, output)]
        return output

    def run(self, peptides, action):
        enc_peptides = self._preprocess_peptides(peptides)
          
        if action == Action.predict:
            predictions = self._predict(enc_peptides)
            output = self._build_output(peptides, 
                                        predictions, 
                                        self.model_config.output_labels)

        else:
            self._check_encoding_permission()
            encodings = self._encode(enc_peptides) 
            output = self._build_output(peptides, encodings)

        return output


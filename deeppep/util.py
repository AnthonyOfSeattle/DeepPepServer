from re import sub
from json import load
from os import environ, path
from glob import glob
from .types import PreprocessingConfig, ModelSpec

def get_app_config():
    config = {}
    config["app_dir"] = path.dirname(path.realpath(__file__))

    # Model locality variables
    config["model_dir_default"] = path.join(config["app_dir"], "models")
    config["model_dir_user"] = environ.get("DEEPPEP_MODEL_DIR")

    return config

def load_model_spec(spec_file):
    raw_spec = load(open(spec_file, "r"))
    
    model_file_base = sub("\.spec\.json$", "", spec_file)
    raw_spec["config_path"] = model_file_base + ".config.json"
    raw_spec["weight_path"] = model_file_base + ".weights.h5"
    
    valid_spec = ModelSpec(**raw_spec)
    return valid_spec

def load_all_specs(model_dir):
    if model_dir is None:
        return {}
    else:
        assert path.exists(model_dir)

    model_spec_iter = map(
        load_model_spec,
        glob(path.join(model_dir, "*.spec.json"))
        )

    model_spec_dict = {spec.model_name : spec 
                       for spec in model_spec_iter}
    return model_spec_dict

def get_model_info():
    app_config = get_app_config()
    model_info = load_all_specs(app_config["model_dir_default"])
    if app_config["model_dir_user"]:
        model_info.update(load_all_specs(app_config["model_dir_user"]))

    return model_info

def merge_configs(left, right):
    # Copy to maintain read only
    left_dict = left.dict()
    right_dict = right.dict()

    # Pop out vocab dict and copy
    merged_vocab = left_dict.pop("vocab").copy()
    merged_vocab.update(right_dict.pop("vocab"))

    # Create final merged config
    merged = left_dict
    merged.update(right_dict)
    merged["vocab"] = merged_vocab

    return PreprocessingConfig(**merged)

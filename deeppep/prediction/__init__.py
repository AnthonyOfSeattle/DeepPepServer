from .manager import PredictionManager

PREBUILT_CONFIG = {
    "__default__": {"max_vocab_dim" : 26,
                    "seq_len"       : 75,
                    "one_hot"       : False,
                    "config_path"   : "",
                    "weight_path"   : ""},

    "phospho_rt" : {"config_path" : "deeppep/prediction/models/phospho_rt_config.json",
                    "weight_path" : "deeppep/prediction/models/phospho_rt_weights.h5"},
}

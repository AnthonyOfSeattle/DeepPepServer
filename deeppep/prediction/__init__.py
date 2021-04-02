from .manager import PredictionManager

PREBUILT_CONFIG = {
    "rt_gru_512" : {
        "pre_config"     : {},
        "config_path"    : "deeppep/prediction/models/rt_gru_512.config.json",
        "weight_path"    : "deeppep/prediction/models/rt_gru_512.weights.h5",
        "property"       : "rt",
        "output_labels"  : ["rt"],
        "allow_encoding" : True,
        "public"         : True
        },
    "phospho_rt_gru_512" : {
        "pre_config"     : {"vocab" : {"S[80]": 24,
                                       "T[80]": 25,
                                       "Y[80]": 26},
                            "max_vocab_dim" : 26,
                            "seq_len" : 75},
        "config_path"    : "deeppep/prediction/models/phospho_rt_gru_512.config.json",
        "weight_path"    : "deeppep/prediction/models/phospho_rt_gru_512.weights.h5",
        "property"       : "rt",
        "output_labels"  : ["rt"],
        "allow_encoding" : True,
        "public"         : True
        },
    "human_phosphopedia_rt" : {
        "pre_config"     : {"vocab" : {"S[80]": 24, 
                                       "T[80]": 25, 
                                       "Y[80]": 26},
                            "max_vocab_dim" : 26,
                            "seq_len" : 75},
        "config_path"    : "deeppep/prediction/models/human_phosphopedia_rt.config.json",
        "weight_path"    : "deeppep/prediction/models/human_phosphopedia_rt.weights.h5",
        "property"       : "rt",
        "output_labels"  : ["rt"],
        "allow_encoding" : False,
        "public"         : True
        },
    "charge_gru_128" : {
        "pre_config"     : {},
        "config_path"    : "deeppep/prediction/models/charge_gru_128.config.json",
        "weight_path"    : "deeppep/prediction/models/charge_gru_128.weights.h5",
        "property"       : "charge",
        "output_labels"  : ["z1", "z2", "z3", "z4", "z5"],
        "allow_encoding" : True,
        "public"         : True
        },

}

PREBUILT_CONFIG["rt"] = PREBUILT_CONFIG["rt_gru_512"]
PREBUILT_CONFIG["phospho_rt"] = PREBUILT_CONFIG["phospho_rt_gru_512"]
PREBUILT_CONFIG["charge"] = PREBUILT_CONFIG["charge_gru_128"]

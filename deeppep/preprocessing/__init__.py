from .manager import GLOBAL_VOCAB, PreprocessingManager

DEFAULT_PREPROCESSING_CONFIG = {
    "pattern"       : "[A-Zn][^A-Zn]*",
    "vocab"         : GLOBAL_VOCAB,
    "max_vocab_dim" : 23,
    "seq_len"       : 50,
    "one_hot"       : False
}

def merge_configs(left, right):
    merged = left.copy()
    merged.update(right)
    
    # Ensure vocab compliance
    if "vocab" in left or "vocab" in right:
        merged["vocab"] = left.get("vocab", {}).copy()
        vocab_update = right.get("vocab", {}).copy()
        merged["vocab"].update(vocab_update)

    return merged

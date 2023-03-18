from model_utterance import ModelUtterances
from statistics import mean, median, mode
from collections import Counter

def load(load_path: str, remove_fluent=False):
    ret = ModelUtterances()
    return ret.from_txt(load_path, remove_fluent)

def get_stats(utterances: ModelUtterances):
    num_disfl_per_utter = []
    avg_disfl_len_per_utter = []
    all_insertion_idx = []
    all_pos_patterns = []
    all_long_pos_patterns = []
    for utter in utterances.utterances:
        num_disfl_per_utter.append(len(utter.disfluencies_arr))
        pos_patterns = [" ".join(pos_tags) for pos_tags in utter.disfluencies_pos_arr]
        long_pos_patterns = [pos_pattern for pos_pattern in pos_patterns if len(pos_pattern.split()) > 1]
        all_pos_patterns += pos_patterns
        all_long_pos_patterns += long_pos_patterns
        avg_disfl_len = mean([len(disfl) for disfl in utter.disfluencies_arr]) if len(utter.disfluencies_arr) else 0
        avg_disfl_len_per_utter.append(avg_disfl_len)
        all_insertion_idx += utter.disfluency_insertion_idxs_arr
    
    avg_num_disfl_per_utter = mean(num_disfl_per_utter)
    med_num_disfl_per_utter = median(num_disfl_per_utter)
    mod_num_disfl_per_utter = mode(num_disfl_per_utter)

    avg_disfl_len = mean(avg_disfl_len_per_utter)
    
    k = 3
    k_idx = Counter(all_insertion_idx).most_common(k)
    k_num_disfl = Counter(num_disfl_per_utter).most_common(k)
    k_pos = Counter(all_pos_patterns).most_common(k)
    k_pos_long = Counter(all_long_pos_patterns).most_common(k)

    return {
        "avg_num_disfl": avg_num_disfl_per_utter,
        "med_num_disfl": med_num_disfl_per_utter,
        "mod_num_disfl": mod_num_disfl_per_utter,
        "top_k_num_disfl": k_num_disfl,
        "avg_disfl_len": avg_disfl_len,
        "top_k_insertion_idxs": k_idx,
        "top_k_pos_patterns": k_pos,
        "top_k_pos_patterns_long": k_pos_long,
    }

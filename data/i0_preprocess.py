from data.utterance import Utterance, Utterances
import csv

def create_i0_indices(utterances: Utterances):
    all_i0_indices = {}
    for id, utterance in utterances.utterances.items():
        fluent = utterance.fluent
        dis_idxs = utterance.disfluent_insertion_idxs
        dis_words = utterance.disfluent_words

        total_words = len(fluent) + sum([len(arr) for arr in dis_words])
        i0_indices = ["0"] * len(fluent)
        dis_idxs.sort(reverse=True)
        for i, idx_str in enumerate(dis_idxs):
            if idx_str != '':
                idx = int(idx_str)
                n = len(dis_words[-(i+1)])
                if idx >= len(fluent):
                    i0_indices += ["I"] * n
                else:
                    i0_indices[idx:idx] = ["I"] * n
        all_i0_indices[id] = i0_indices
        assert len(i0_indices) == total_words
    return all_i0_indices

def add_i0_to_utterances(i0_indices, utterances: Utterances):
    for id, i0 in i0_indices.items():
        utterance = utterances.utterances[id]
        utterance.i0 = i0
        utterances.utterances[id] = utterance
    return utterances
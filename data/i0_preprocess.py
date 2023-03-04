from data.utterance import Utterance, Utterances
import csv

def i0_preprocess(csv_path, export=True):
    """
    """
    utterances = Utterances(csv_path)
    idxs = create_i0_indices(utterances)
    utterances = add_i0_to_utterances(idxs, utterances)

    if export:
    # TODO: call export csv to save i0, temp simply print
        for i, i0 in idxs.items():
            print(" ".join(i0))
    return utterances

def create_i0_indices(utterances: Utterances):
    all_i0_indices = {}
    for id, utterance in utterances.utterances.items():
        fluent = utterance.fluent
        dis_idxs = []
        if utterance.disfluent_insertion_idxs[0] != '':
            dis_idxs = [int(i) for i in utterance.disfluent_insertion_idxs]
        dis_words = [i for i in utterance.disfluent_words if i]
        total_words = len(fluent) + sum([len(arr) for arr in dis_words])
        i0_indices = ["0"] * len(fluent)
        dis_idxs.sort(reverse=True)
        for i, idx in enumerate(dis_idxs):
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
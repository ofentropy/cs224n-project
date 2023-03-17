from data.utterance import Utterance, Utterances
import csv

def io_preprocess(csv_path, export=True):
    """
    """
    utterances = Utterances(csv_path)
    idxs = create_io_indices(utterances)
    utterances = add_io_to_utterances(idxs, utterances)

    if export:
    # TODO: call export csv to save io, temp simply print
        for i, io in idxs.items():
            print(" ".join(io))
    return utterances

def create_io_indices(utterances: Utterances):
    all_io_indices = {}
    for id, utterance in utterances.utterances.items():
        fluent = utterance.fluent
        dis_idxs = []
        if utterance.disfluent_insertion_idxs[0] != '':
            dis_idxs = [int(i) for i in utterance.disfluent_insertion_idxs]
        dis_words = [i for i in utterance.disfluent_words if i]
        total_words = len(fluent) + sum([len(arr) for arr in dis_words])
        io_indices = ["O"] * len(fluent)
        dis_idxs.sort(reverse=True)
        for i, idx in enumerate(dis_idxs):
            n = len(dis_words[-(i+1)])
            if idx >= len(fluent):
                io_indices += ["I"] * n
            else:
                io_indices[idx:idx] = ["I"] * n
        all_io_indices[id] = io_indices
        assert len(io_indices) == total_words
    return all_io_indices

def add_io_to_utterances(io_indices, utterances: Utterances):
    for id, io in io_indices.items():
        utterance = utterances.utterances[id]
        utterance.io = io
        utterances.utterances[id] = utterance
    return utterances
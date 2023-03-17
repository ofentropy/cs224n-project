from data.utterance import Utterance, Utterances
from data.naive_preprocess import normalize
from data.io_preprocess import *
from data.keys import *
import re

def split_into_sentences(text: str):
    return re.split('[!?\.]', text)

def lard_preprocess(load_path: str, save_path: str):
    lard_input_raw = []
    with open(save_path, 'w', newline='') as csv_file:
        fieldnames = ["id", "disfluent_sentence", "fluent_sentence", "io_indexing"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        utterances = Utterances(load_path)
        if io_INDEX_KEY not in utterances.utterances.keys():
            utterances = io_preprocess(load_path, export=False)
        for id, utterance in utterances.utterances.items():
            disfluent_full_raw = utterance.metadata[TEXT_KEY]
            # split disfluency into sentences using ".", "!" and "?" as delimiters
            disfluent_sentences = [normalize(sentence) for sentence in split_into_sentences(disfluent_full_raw) if sentence]
            rows = split_io_into_sentences(disfluent_sentences, utterance)
            for row in rows:
                lard_input_raw.append(row)
                writer.writerow(row)
    return lard_input_raw        

def split_io_into_sentences(disfluent_sentences, utterance: Utterance):
    fluent_sentences = [normalize(sentence).split() for sentence in split_into_sentences(utterance.fluent) if sentence]
    io_full = utterance.io
    id = utterance.id
    dis_idxs = []
    if utterance.disfluent_insertion_idxs[0] != '':
        dis_idxs = [int(i) for i in utterance.disfluent_insertion_idxs]
    io_sentences = []
    dis_idxs.sort()
    print(dis_idxs)
    i = 0
    fluent_i = 0
    rows = []
    for sentence in disfluent_sentences:
        n = len(sentence.split())
        io = io_full[i:i+n]
        print(i, i+n, len(io), n)
        row = {
            "id": id,
            "disfluent_sentence": " ".join(sentence.split()),
            "fluent_sentence": "",
            "io_indexing": " ".join(io)
        }
        if "0" in io:
            print(row, fluent_i, len(fluent_sentences))
            row["fluent_sentence"] = " ".join(fluent_sentences[fluent_i])
            fluent_i += 1
        i += n
        rows.append(row)
    return rows
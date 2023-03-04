import csv
from data.naive_preprocess import normalize
from data.keys import *

def to_array(raw: str, delimiter = ";"):
    # lowercase all + remove punctuation other than apostrophes
    arr = raw.split(delimiter)
    arr = [normalize(element) for element in arr]
    return arr

class Utterance:
    def __init__(self, metadata: dict):
        self.id = metadata[ID_KEY]
        self.fluent = metadata[FLUENT_KEY]
        
        self.disfluent_insertion_idxs = to_array(metadata[DISFLUENCY_IDX_KEY], delimiter=";")
        
        self.disfluent_words = []
        for disfluent_phrase in to_array(metadata[DISFLUENCY_WORDS_KEY], delimiter=";"):
            disfluent_phrase_arr = to_array(disfluent_phrase, delimiter=None)
            self.disfluent_words.append(disfluent_phrase_arr)
        
        self.disfluent_dict = {}
        for i, idx in enumerate(self.disfluent_insertion_idxs):
            self.disfluent_dict[idx] = self.disfluent_words[i]
        
        if TEXT_KEY in metadata.keys():
            self.disfluent = to_array(metadata[TEXT_KEY])
        
        self.metadata = metadata

class Utterances:
    def __init__(self, csv_path: str):
        self.metadatas = {}
        self.utterances_list = []
        self.utterances = {}
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                utterance = Utterance(row)
                self.utterances_list.append(utterance)
                self.utterances[row[ID_KEY]] = utterance
                self.metadatas[row[ID_KEY]] = row
    
    def __len__(self):
        return len(self.utterances_list)

    def get_utterances_dict(self):
        return self.utterances
    
    def get_utterances_list(self):
        return self.utterances_list

    def get_all_fluent_and_disfluent(self):
        fluent, disfluent = []
        for utterance in self.utterances_list:
            fluent.append(utterance.fluent)
            disfluent.append(utterance.disfluent)
        return fluent, disfluent

    def get_metadatas_dict(self):
        return self.metadatas

    def get_utterance_by_id(self, id: str):
        return self.utterances[id]

    def get_metadata_by_id(self, id: str):
        return self.metadatas[id]
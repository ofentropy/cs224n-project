import csv
from data.keys import ID_KEY, DISFLUENCY_IDX_KEY, DISFLUENCY_WORDS_KEY, FLUENT_KEY, TEXT_KEY
from data.utterance import to_array


class ModelUtterance:
    def __init__(self, metadata: dict):
        self.fluent = metadata[FLUENT_KEY]
       
        self.disfluent_insertion_idxs = to_array(metadata[DISFLUENCY_IDX_KEY], delimiter=";")
        
        self.disfluent_words = []
        for disfluent_phrase in to_array(metadata[DISFLUENCY_WORDS_KEY], delimiter=";"):
            disfluent_phrase_arr = to_array(disfluent_phrase, delimiter="")
            self.disfluent_words.append(disfluent_phrase_arr)
        
        self.disfluent_dict = {}
        for i, idx in enumerate(self.disfluent_insertion_idxs):
            self.disfluent_dict[idx] = self.disfluent_words[i]
        
        self.disfluent = to_array(metadata[TEXT_KEY])
        
        # self.metadata = metadata

class ModelUtterances:
    def __init__(self):
        self.utterances = {}
        self.utterances_list = []

    def __len__(self):
        return len(self.utterances_list)
    
    def append(self, utterance: ModelUtterance):
        self.utterances_list.append(utterance)
        self.utterances[utterance[ID_KEY]] = utterance

    def from_csv(self, csv_path: str):
        self.utterances = {}
        self.utterances_list = []
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                utterance = ModelUtterance(row)
                self.utterances_list.append(utterance)
                self.utterances[row[ID_KEY]] = utterance
    
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

    def get_utterance_by_id(self, id: str):
        return self.utterances[id]
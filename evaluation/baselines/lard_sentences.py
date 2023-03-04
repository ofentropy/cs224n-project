import csv

class LARDSentence:
    def __init__(self, metadata: dict):
        self.fluent = metadata["fluent_sentence"]
        self.disfluent = metadata["disfluent_sentence"]
        self.id = metadata["id"]
        self.i0 = metadata["i0_indexing"]
        self.metadata = metadata

    def __repr__(self):
        return str(self.metadata)

    def __add__(self, val2):
        s1 = LARDSentences()
        s1.from_metadata(self.metadata)
        s2 = LARDSentences()
        s2.from_metadata(val2.metadata)
        return s1+s2


class LARDSentences:
    def __init__(self, csv_path=None):
        self.sentences_list = []
        self.sentences = {}
        if csv_path:
            self.from_csv(csv_path, ret=False)
    
    def from_metadata(self, metadatas: list):
        for metadata in metadatas:
            sentence = LARDSentence(metadata)
            if "I" in sentence.i0: # skip sentences that do not have disfluencies
                self.sentences_list.append(sentence)
                sentences = self.sentences.get(metadata["id"], [])
                sentences.append(sentence)
                self.sentences[metadata["id"]] = sentences
        return self

    def from_csv(self, csv_path: str, ret=True):
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                sentence = LARDSentence(row)
                if "I" in sentence.i0: # skip sentences that do not have disfluencies
                    self.sentences_list.append(sentence)
                    sentences = self.sentences.get(row["id"], [])
                    sentences.append(sentence)
                    self.sentences[row["id"]] = sentences
        return self
    
    def __add__(self, val2):
        self.sentences_list = self.sentences_list + val2.sentences_list
        for key, value in val2.sentences.items():
            temp = self.sentences.get(key, [])
            temp += value
            self.sentences[key] = temp
        return self

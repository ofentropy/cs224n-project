import csv
# from nltk import pos_tag # uncomment in colab

class ModelUtterance(object):
    def __init__(self, metadata):
        self.metadata = metadata
        self.text_arr = metadata["text"]
        self.io_arr = metadata["io"]
        self.pos_arr = metadata["pos"]
        self.full_str = " ".join(self.text_arr)
        self.get_fluent()
    
    def get_fluent(self):
        self.fluent_arr = []
        self.disfluencies_arr = []
        self.disfluencies_pos_arr = []
        self.disfluencies_str = []
        self.disfluency_insertion_idxs_arr = []
        disfl = []
        disfl_pos = []

        for i, word in enumerate(self.text_arr):
            if self.io_arr[i] == "O" or self.io_arr[i] == "0":
                self.fluent_arr.append(word)
                if len(disfl) > 0:
                    self.disfluencies_arr.append(disfl)
                    self.disfluencies_pos_arr.append(disfl_pos)
                    disfl = []
                    disfl_pos = []
            elif self.io_arr[i] == "I":
                if len(disfl) == 0:
                    self.disfluency_insertion_idxs_arr.append(i)
                disfl.append(word)
                disfl_pos.append(self.pos_arr[i])
        if len(disfl) > 0:
            self.disfluencies_arr.append(disfl)
            self.disfluencies_pos_arr.append(disfl_pos)

        self.fluent_str = " ".join(self.fluent_arr)
        for disfl_arr in self.disfluencies_arr:
            self.disfluencies_str.append(" ".join(disfl_arr))
    
class ModelUtterances(object):
    def __init__(self):
        self.metadatas = None
        self.utterances = None

    def from_txt(self, load_path: str, remove_fluent=False):
        self.metadatas = []
        self.utterances = []
        with open(load_path, "r") as f:
            lines = f.readlines()
        
        metadata = {}
        i = 0
        for line in lines:
            if line.strip() != '':
                line = line.strip()
                line_arr = line.split("\t")
                if (i+1)%3 == 1:
                    metadata["text"] = line_arr
                elif (i+1)%3 == 2:
                    metadata["pos"] = line_arr
                    if len(set(metadata["pos"])) == 1 and "P" in set(metadata["pos"]):
                        metadata["pos"] = [pos[1] for pos in pos_tag(metadata["text"])]
                elif (i+1)%3 == 0:
                    metadata["io"]  = line_arr
                    if not remove_fluent or "I" in metadata["io"]:
                        self.metadatas.append(metadata)
                        self.utterances.append(ModelUtterance(metadata))
                    metadata = {}
                i += 1
        
        return self
    

    def from_csv(self, csv_path: str, remove_fluent=False, results=False):
        self.metadatas = []
        self.utterances = []
        disfluent_key = "disfluent_original"
        if results:
            disfluent_key = "disfluent_sentence"
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                metadata = {}
                metadata["text"] = row[disfluent_key].split()
                metadata["pos"] = pos_tag(metadata["text"])
                metadata["io"] = row["io_indexing"].replace("0", "O").split()
                utterance = ModelUtterance(metadata)
                self.metadatas.append(metadata)
                self.utterances.append(utterance)
        return self
        
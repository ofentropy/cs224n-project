# from nltk.tokenize.treebank import TreebankWordDetokenizer
from model_utterance import ModelUtterance, ModelUtterances
from python_files.disfluency_generation import LARD # requires https://github.com/tatianapassali/artificial-disfluency-generation
from nltk import pos_tag
from nltk.translate.bleu_score import sentence_bleu
import nltk
from statistics import mean
nltk.download('wordnet')

lard = LARD()

def convert_annotations(annotations):
    return (" ".join(annotations).replace("D", "I").replace("F", "O")).split()

def generate_lard_replacements(utterances: ModelUtterances):
    ret = ModelUtterances()
    ret.utterances = []
    ret.metadatas = []
    for utter in utterances.utterances:
        fluent_arr = utter.fluent_arr
        if fluent_arr:
            fluent_str = " ".join(fluent_arr)
            output = lard.create_replacements(fluent_str)
            if output[0]:
                metadata = {}
                metadata["text"] = output[0].split()
                metadata["io"] = convert_annotations(output[3])
                metadata["pos"] = [pos[1] for pos in pos_tag(output[0].split())]
                metadata["gold"] = utter.text_arr
                utterance = ModelUtterance(metadata)
                ret.metadatas.append(metadata)
                ret.utterances.append(utterance)
    return ret

def average_bleu_disfl_sentence(outputs: ModelUtterances):
    bleus = []
    for utter in outputs.utterances:
        hypothesis = utter.metadata["text"]
        reference = utter.metadata["gold"]
        bleu = sentence_bleu([reference], hypothesis)
        bleus.append(bleu)
    return mean(bleus)

def export_outputs(outputs: ModelUtterances, save_path="lard_swda_test.txt"):
    with open(save_path, "w") as f:
        for utter in outputs.utterances:
            if utter.text_arr:
                text = '\t'.join(utter.text_arr)
                pos = '\t'.join(utter.pos_arr)
                io = '\t'.join(utter.io_arr)
                f.write(text+"\n")
                f.write(pos+"\n")
                f.write(io+"\n")
                f.write("\n")
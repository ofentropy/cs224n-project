from evaluation.baselines.lard_sentences import LARDSentences, LARDSentences
from python_files.disfluency_generation import LARD # requires https://github.com/tatianapassali/artificial-disfluency-generation
from nltk.translate.bleu_score import sentence_bleu # requires installing nltk
import csv

import nltk
nltk.download('wordnet')

lard = LARD()

def lard_output_to_dict(lard_output, i0_indexing, id, disfluent_original):
    return { "disfluent_sentence": lard_output[0],
            "fluent_tokens": lard_output[1],
            "disfluent_tokens": lard_output[2],
            "annotations": lard_output[3],
            "disfl_type": lard_output[4],
            "i0_indexing": i0_indexing,
            "id": id,
            "disfluent_original":disfluent_original,
    }

def generate_lard_replacements(sentences: LARDSentences):
    id_to_output = {}
    has_output = LARDSentences()
    for sentence in sentences.sentences_list:
        id = sentence.id
        fluent_sentence = sentence.fluent
        if fluent_sentence:
            print("FLUENT_SENTENCE: " + fluent_sentence)
            output = lard.create_replacements(fluent_sentence)
            if output[0]:
              sentence_temp = LARDSentences()
              has_output += sentence_temp.from_metadata([sentence.metadata])
              print("OUTPUT: " + output[0])
            else:
              print("NO OUTPUT.")
            output = lard_output_to_dict(output, sentence.i0, id, sentence.disfluent)
            temp = id_to_output.get(id, [])
            temp.append(output)
            id_to_output[id] = temp
    return id_to_output, has_output

def generate_lard_restarts(sentences: LARDSentences):
    id_to_output = {}
    has_output = LARDSentences()
    for i in range(len(sentences.sentences_list)):
        for j in range(len(sentences.sentences_list)):
            if i != j:
                sen_1 = sentences.sentences_list[i]
                sen_2 = sentences.sentences_list[j]
                id = sen_1.id
                fluent_1 = sen_1.fluent
                fluent_2 = sen_2.fluent
                output = lard.create_restarts(fluent_1, fluent_2)
                if output[0]:
                    sentence_temp = LARDSentences()
                    has_output += sentence_temp.from_metadata([sen_1.metadata])
                    print("OUTPUT: " + output[0])
                else:
                    print("NO OUTPUT.")
                output = lard_output_to_dict(output, sen_1.i0, id, sen_1.disfluent)
                temp = id_to_output.get(id, [])
                temp.append(output)
                id_to_output[id] = temp
    return id_to_output, has_output

def get_disfluent_parts(disfl_arr, i0_arr):
    assert len(disfl_arr) == len(i0_arr)

    tokens = []
    for i, i0_val in enumerate(i0_arr):
        if i0_val == "I" or i0_val == "D":
            tokens.append(disfl_arr[i])
    return tokens

def average_bleu_disfl_parts(outputs: dict):
    id_to_bleu = {}
    nons = 0
    total = 0
    for id, output_arrays in outputs.items():
        bleu_sum_per_id = 0
        for output in output_arrays: 
          total+=1
          if output["disfluent_tokens"]:
            hypothesis = get_disfluent_parts(output["disfluent_tokens"], output["annotations"])
            reference = get_disfluent_parts(output["disfluent_original"].split(), output["i0_indexing"].split())
            if not reference:
                reference = [""]
            bleu = sentence_bleu(reference, hypothesis)
            # print(bleu)
            bleu_sum_per_id += bleu
          else:
              nons += 1
        bleu_sum_per_id /= len(output_arrays)
        id_to_bleu[id] = bleu_sum_per_id
    return sum(list(id_to_bleu.values()))/len(id_to_bleu.keys()), nons/total

def average_bleu_disfl_sentence(outputs: dict):
    id_to_bleu = {}
    nons = 0
    total = 0
    for id, output_arrays in outputs.items():
        bleu_sum_per_id = 0
        for output in output_arrays: 
          total+=1
          hypothesis = output["disfluent_tokens"]
          reference = output["disfluent_original"].split()
          if not hypothesis:
              nons += 1
          else:
            bleu = sentence_bleu(reference, hypothesis)
            # print(bleu)
            bleu_sum_per_id += bleu
        bleu_sum_per_id /= len(output_arrays)
        id_to_bleu[id] = bleu_sum_per_id
    return sum(list(id_to_bleu.values()))/len(id_to_bleu.keys()), nons/total

#def create_references_hypotheses(outputs: dict):
#    hypotheses = []
#    references = []
#    for id, output_arrays in outputs.items():
#        for output in output_arrays:
#            hypothesis = output["disfluent_tokens"]
#            reference = output["disfluent_original"].split()
#            if hypothesis:
#              hypotheses.append(output)
#              references.append(reference)
#    return references, hypotheses

def export_outputs(save_path: str, outputs: list):
    with open(save_path, 'w', newline='') as csv_file:
        fieldnames = ["id", "disfluent_sentence", "fluent_tokens", "disfluent_tokens", "annotations", "disfl_type", "i0_indexing", "disfluent_original"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for _, output_arrays in outputs.items():
            for output in output_arrays:
                writer.writerow(output)

### UNCOMMENT TO RUN LARD ###
# first20_sentences = LARDSentences(csv_path="data/tables/lard_first20.csv")
# last20_sentences = LARDSentences(csv_path="data/tables/lard_last20.csv")
# id2op_1, hop_1 = generate_lard_replacements(first20_sentences)
# id2op_2, hop_2 = generate_lard_replacements(last20_sentences)
# restarts_1 = generate_lard_restarts(hop_1)

### UNCOMMENT TO EXPORT LARD RESULTS TO A CSV###
#export_outputs("lardresults_first20.csv", id2op_1)
#export_outputs("lardresults_last20.csv", id2op_2)

### UNCOMMENT TO EVALUATE LARD FOR BLEU###
#print(average_bleu_disfl_parts(id2op_1))
#print(average_bleu_disfl_parts(id2op_2))
#print(average_bleu_disfl_sentence(id2op_1))
#print(average_bleu_disfl_sentence(id2op_2))
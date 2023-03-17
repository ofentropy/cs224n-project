from nltk import pos_tag_sents
# may need to install nltk packages first!
from data.naive_preprocess import normalize
from data.utterance import Utterance
from model_utterance import ModelUtterances, ModelUtterance
from math import lcm
import csv

def export_results(results: ModelUtterances, write_path: str):
    #TODO: write csv export
    pass

def calculate_ratio_of_disfluent_words(utterance):
    """
    @param utterance
    @return tuple
    """
    full = utterance.disfluent
    disfluent_phrases = utterance.fluent

    total_words = len(full)
    total_disfluent = sum([len(arr) for arr in disfluent_phrases])
    
    return (total_disfluent,total_words)

def calculate_disfluent_grammar_pattern(disfluencies):
    # TODO: figure out how to calculate disfluent grammar pattern top 5
    pass

def compare_insertion_points(test: ModelUtterance, reference: Utterance, strict=True):
    # TODO: compare the arrays of insertion points
    test_idxs = test.disfluent_insertion_idxs
    ref_idxs = reference.disfluent_insertion_idxs

    if not strict:
        pass
    else:
        pass
        
    pass

def compare_disfluent_ratio(test: ModelUtterance, reference: Utterance):
    # TODO: figure out how to compare ratios
    pass
    #test_ratio = calculate_ratio_of_disfluent_words(test)
    #reference_ratio = calculate_ratio_of_disfluent_words(reference)
    #lcm = lcm(test_ratio[1], reference_ratio[1])
    #test_ratio = lcm/test_ratio[0]
    #reference_ratio = lcm/reference_ratio[0]
    #if test_ratio == reference_ratio:
    #    pass
    #elif test_ratio < reference_ratio:
    #    pass
    #else:
    #    pass 

def compare_disfluent_grammar(test: ModelUtterance, reference: Utterance):
    # TODO: compare disfluent grammar
    pass

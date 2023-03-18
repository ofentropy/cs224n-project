from nltk.translate.bleu_score import sentence_bleu
from data.utterance import Utterance, Utterances
from archive.model_utterance import ModelUtterance, ModelUtterances
import archive.helpers as helpers
from statistics import mean, median

# Import ground truth
csv_path = None
test_utterances = Utterances(csv_path)
inputs, _ = test_utterances.get_all_fluent_and_disfluent()

# TODO: add code to run LARD + baseline model

LARD_results = ModelUtterances()
baseline_results = ModelUtterances()

# Export results to CSV
LARD_csv_path = None
baseline_csv_path = None

helpers.export_results(LARD_results, LARD_csv_path)
helpers.export_results(baseline_results, baseline_csv_path)

# evaluation metrics
def get_bleu_metrics(results: ModelUtterances):
    """
    @param results ModelUtterances
    @return tuple(list, float, float): scores, mean, median of bleu scores
    """
    scores = []
    for id, utterance in results.utterances.items():
        generated_disfluency = utterance.disfluent
        ground_truth = test_utterances.get_utterance_by_id(id).disfluent
        scores.append(sentence_bleu(ground_truth, generated_disfluency))
    return scores, mean(scores), median(scores)

def insertion_points():
    # TODO: evaluate insertion points accuracy
    pass

def grammar_patterns():
    # TODO: evaluate grammar patterns of disfluency phrases
    pass
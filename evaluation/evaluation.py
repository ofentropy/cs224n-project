from nltk.translate.bleu_score import sentence_bleu
from data.utterance import Utterance, Utterances
from model_utterance import ModelUtterance, ModelUtterances
import helpers

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
def get_average_bleu(model="LARD"):
    results = None
    if model == "LARD":
        results = LARD_results
    elif model == "baseline":
        results = baseline_results
    else:
        print("Unknown model")
        return
    score = 0
    for id, utterance in results.utterances.items():
        generated_disfluency = utterance.disfluent
        ground_truth = test_utterances.get_utterance_by_id(id).disfluent
        score += sentence_bleu(ground_truth, generated_disfluency)
    return float(score/len(results))

def insertion_points():
    # TODO: evaluate insertion points accuracy
    pass

def grammar_patterns():
    # TODO: evaluate grammar patterns of disfluency phrases
    pass
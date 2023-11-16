from .bleu import BLEU
from .rouge import ROUGE
from .chrf import CHRF
from .function_execution import FunctionExecution
from .prefix_match import PrefixMatch
from .exact_match import ExactMatch
from .log_prob import LogProb
from .f1_score import F1Score
from .log_prob_mc2 import LogProbMC2

METRICS_REGISTRY = {
    "bleu": BLEU,
    "rouge": ROUGE,
    "chrf": CHRF,
    "prefix_match": PrefixMatch,
    "exact_match": ExactMatch,
    "log_prob": LogProb,
    "log_prob_mc2": LogProbMC2,
    "f1_score": F1Score,
    "function_execution": FunctionExecution,
}


def get_metric(metric_name):
    return METRICS_REGISTRY[metric_name]

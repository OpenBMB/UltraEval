from .bleu import BLEU
from .chrf import CHRF
from .exact_match import ExactMatch
from .f1_score import F1Score
from .function_execution import FunctionExecution
from .gaokaobench_match import GaoKaoBenchMatch
from .log_prob import LogProb
from .log_prob_mc2 import LogProbMC2
from .prefix_match import PrefixMatch
from .rouge import ROUGE

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
    "gaokaobench_match": GaoKaoBenchMatch,
}


def get_metric(metric_name):
    return METRICS_REGISTRY[metric_name]

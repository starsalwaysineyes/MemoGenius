from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Set

Interactions = Dict[int, List[int]]


@dataclass
class EvalResult:
    recall_at_k: float
    ndcg_at_k: float


def _dcg(rels: List[int]) -> float:
    return sum((2**r - 1) / math.log2(i + 2) for i, r in enumerate(rels))


def evaluate_topk(
    user_emb: List[List[float]],
    item_emb: List[List[float]],
    train_interactions: Interactions,
    test_interactions: Interactions,
    k: int = 20,
) -> EvalResult:
    recalls, ndcgs = [], []
    all_items = set(range(len(item_emb)))

    for u, test_items in test_interactions.items():
        if not test_items:
            continue
        train_set: Set[int] = set(train_interactions.get(u, []))
        cand = list(all_items - train_set)
        if not cand:
            continue

        scores = []
        for i in cand:
            s = sum(a * b for a, b in zip(user_emb[u], item_emb[i]))
            scores.append((s, i))
        scores.sort(reverse=True)
        topk = [i for _, i in scores[:k]]

        hit = [1 if i in set(test_items) else 0 for i in topk]
        recall = sum(hit) / len(set(test_items))
        ideal = [1] * min(len(set(test_items)), k)
        ndcg = _dcg(hit) / (_dcg(ideal) + 1e-8)
        recalls.append(recall)
        ndcgs.append(ndcg)

    if not recalls:
        return EvalResult(0.0, 0.0)
    return EvalResult(sum(recalls) / len(recalls), sum(ndcgs) / len(ndcgs))

from __future__ import annotations

import math
from dataclasses import dataclass

from .interfaces import Matrix
from .utils import dot


@dataclass
class ObjectiveWeights:
    rec: float = 1.0
    cl: float = 0.1
    uniform: float = 0.05
    reg: float = 1e-4


@dataclass
class LossBreakdown:
    total: float
    rec_error: float
    cl_error: float
    uniform_error: float
    reg_error: float


def bpr_recommendation_error(user_emb: Matrix, pos_emb: Matrix, neg_emb: Matrix) -> float:
    vals = []
    for u, p, n in zip(user_emb, pos_emb, neg_emb):
        diff = dot(u, p) - dot(u, n)
        vals.append(-math.log(1.0 / (1.0 + math.exp(-diff)) + 1e-8))
    return sum(vals) / len(vals)


def node_uniformity_error(z: Matrix, tau: float = 2.0) -> float:
    # Uniformity term: log E[e^{-tau||zi-zj||^2}], lower is better spread.
    if len(z) < 2:
        return 0.0
    vals = []
    for i in range(len(z)):
        for j in range(i + 1, len(z)):
            dist2 = sum((a - b) ** 2 for a, b in zip(z[i], z[j]))
            vals.append(math.exp(-tau * dist2))
    return math.log(sum(vals) / len(vals) + 1e-8)


def l2_regularization_error(z: Matrix) -> float:
    total = 0.0
    count = 0
    for row in z:
        for v in row:
            total += v * v
            count += 1
    return total / max(count, 1)

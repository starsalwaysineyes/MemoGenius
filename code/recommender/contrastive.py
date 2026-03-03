from __future__ import annotations

import math

from .interfaces import ContrastiveLoss, Matrix
from .utils import dot, l2_norm, softmax, transpose


def _row_normalize(z: Matrix) -> Matrix:
    return [[v / l2_norm(row) for v in row] for row in z]


def _cross_entropy(logits: Matrix, labels):
    total = 0.0
    for i, row in enumerate(logits):
        probs = softmax(row)
        total += -math.log(probs[labels[i]] + 1e-8)
    return total / len(logits)


class InfoNCEContrastiveLoss(ContrastiveLoss):
    """Fixed contrastive error term used by the global objective."""

    def __init__(self, temperature: float = 0.2):
        self.temperature = temperature

    def compute(self, z1: Matrix, z2: Matrix) -> float:
        a, b = _row_normalize(z1), _row_normalize(z2)
        sim = [[dot(x, y) / self.temperature for y in b] for x in a]
        labels = list(range(len(a)))
        return 0.5 * (_cross_entropy(sim, labels) + _cross_entropy(transpose(sim), labels))

from __future__ import annotations

import math
import random
from typing import List

Matrix = List[List[float]]
Vector = List[float]


def randn(rows: int, cols: int, seed: int = 42, scale: float = 0.1) -> Matrix:
    rng = random.Random(seed)
    return [[rng.gauss(0, scale) for _ in range(cols)] for _ in range(rows)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    b_t = list(zip(*b))
    return [[sum(ai * bj for ai, bj in zip(row, col)) for col in b_t] for row in a]


def relu(a: Matrix) -> Matrix:
    return [[max(0.0, v) for v in row] for row in a]


def concat(a: Matrix, b: Matrix) -> Matrix:
    return [ra + rb for ra, rb in zip(a, b)]


def transpose(a: Matrix) -> Matrix:
    return [list(col) for col in zip(*a)]


def mean_matrices(mats: List[Matrix]) -> Matrix:
    n = len(mats)
    rows, cols = len(mats[0]), len(mats[0][0])
    out = [[0.0] * cols for _ in range(rows)]
    for m in mats:
        for i in range(rows):
            for j in range(cols):
                out[i][j] += m[i][j] / n
    return out


def dot(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b))


def l2_norm(a: Vector) -> float:
    return math.sqrt(sum(v * v for v in a) + 1e-8)


def softmax(logits: Vector) -> Vector:
    m = max(logits)
    exps = [math.exp(x - m) for x in logits]
    s = sum(exps) + 1e-8
    return [e / s for e in exps]

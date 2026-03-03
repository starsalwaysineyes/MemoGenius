from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Tuple


Matrix = List[List[float]]
EdgeIndex = List[Tuple[int, int]]
Interactions = Dict[int, List[int]]
Triplets = Dict[str, List[int]]


@dataclass
class GraphBatch:
    x: Matrix
    edge_index: EdgeIndex


class GraphEncoder(ABC):
    @abstractmethod
    def __call__(self, x: Matrix, edge_index: EdgeIndex) -> Matrix:
        raise NotImplementedError


class PositiveNegativeSampler(ABC):
    """Sample (user, positive item, negative item) triplets for recommendation."""

    @abstractmethod
    def sample(self, interactions: Interactions, item_pool: List[int], batch_size: int) -> Triplets:
        raise NotImplementedError


class GraphCLStrategy(ABC):
    """Build two graph views for contrastive learning (node/edge/feature perturbation)."""

    @abstractmethod
    def generate(self, graph: GraphBatch) -> Tuple[GraphBatch, GraphBatch]:
        raise NotImplementedError


class ContrastiveLoss(ABC):
    @abstractmethod
    def compute(self, z1: Matrix, z2: Matrix) -> float:
        raise NotImplementedError


def edge_index_to_adj(edge_index: EdgeIndex, num_nodes: int) -> Matrix:
    adj = [[0.0 for _ in range(num_nodes)] for _ in range(num_nodes)]
    for s, d in edge_index:
        adj[s][d] = 1.0
    for i in range(num_nodes):
        adj[i][i] = 1.0
        row_sum = sum(adj[i])
        if row_sum > 0:
            adj[i] = [v / row_sum for v in adj[i]]
    return adj


def gather_triplets(emb: Matrix, triplets: Triplets):
    users = [emb[i] for i in triplets["users"]]
    pos_items = [emb[i] for i in triplets["pos_items"]]
    neg_items = [emb[i] for i in triplets["neg_items"]]
    return users, pos_items, neg_items

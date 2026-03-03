from __future__ import annotations

import random

from .interfaces import GraphBatch, GraphCLStrategy


def _edge_drop(graph: GraphBatch, drop_rate: float, rng: random.Random) -> GraphBatch:
    kept = [e for e in graph.edge_index if rng.random() > drop_rate]
    return GraphBatch(x=graph.x, edge_index=kept)


def _feature_mask(graph: GraphBatch, mask_rate: float, rng: random.Random) -> GraphBatch:
    x = []
    for row in graph.x:
        x.append([v if rng.random() > mask_rate else 0.0 for v in row])
    return GraphBatch(x=x, edge_index=graph.edge_index)


def _node_drop(graph: GraphBatch, keep_rate: float, rng: random.Random) -> GraphBatch:
    keep_nodes = [i for i in range(len(graph.x)) if rng.random() < keep_rate]
    if not keep_nodes:
        keep_nodes = [0]
    mapping = {node: idx for idx, node in enumerate(keep_nodes)}
    new_edges = [(mapping[s], mapping[d]) for s, d in graph.edge_index if s in mapping and d in mapping]
    return GraphBatch(x=[graph.x[i] for i in keep_nodes], edge_index=new_edges)


class EdgeDropCLStrategy(GraphCLStrategy):
    def __init__(self, drop_rate_a: float = 0.2, drop_rate_b: float = 0.3, seed: int = 42):
        self.drop_rate_a = drop_rate_a
        self.drop_rate_b = drop_rate_b
        self.rng = random.Random(seed)

    def generate(self, graph: GraphBatch):
        return _edge_drop(graph, self.drop_rate_a, self.rng), _edge_drop(graph, self.drop_rate_b, self.rng)


class FeatureMaskCLStrategy(GraphCLStrategy):
    def __init__(self, mask_rate_a: float = 0.2, mask_rate_b: float = 0.3, seed: int = 42):
        self.mask_rate_a = mask_rate_a
        self.mask_rate_b = mask_rate_b
        self.rng = random.Random(seed)

    def generate(self, graph: GraphBatch):
        return _feature_mask(graph, self.mask_rate_a, self.rng), _feature_mask(graph, self.mask_rate_b, self.rng)


class NodeDropCLStrategy(GraphCLStrategy):
    def __init__(self, keep_rate_a: float = 0.9, keep_rate_b: float = 0.8, seed: int = 42):
        self.keep_rate_a = keep_rate_a
        self.keep_rate_b = keep_rate_b
        self.rng = random.Random(seed)

    def generate(self, graph: GraphBatch):
        return _node_drop(graph, self.keep_rate_a, self.rng), _node_drop(graph, self.keep_rate_b, self.rng)


class HybridCLStrategy(GraphCLStrategy):
    """View1: edge-drop, View2: feature-mask (common hybrid CL baseline)."""

    def __init__(self, drop_rate: float = 0.2, mask_rate: float = 0.2, seed: int = 42):
        self.drop_rate = drop_rate
        self.mask_rate = mask_rate
        self.rng = random.Random(seed)

    def generate(self, graph: GraphBatch):
        return _edge_drop(graph, self.drop_rate, self.rng), _feature_mask(graph, self.mask_rate, self.rng)

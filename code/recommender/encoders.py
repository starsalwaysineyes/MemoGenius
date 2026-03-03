from __future__ import annotations

from .interfaces import EdgeIndex, Matrix, edge_index_to_adj
from .utils import concat, matmul, mean_matrices, randn, relu, softmax


class LightGCNEncoder:
    def __init__(self, in_dim: int, emb_dim: int, layers: int = 2, seed: int = 42):
        self.w = randn(in_dim, emb_dim, seed=seed)
        self.layers = layers

    def __call__(self, x: Matrix, edge_index: EdgeIndex) -> Matrix:
        h = matmul(x, self.w)
        adj = edge_index_to_adj(edge_index, len(h))
        embs = [h]
        for _ in range(self.layers):
            h = matmul(adj, h)
            embs.append(h)
        return mean_matrices(embs)


class GraphSAGEEncoder:
    def __init__(self, in_dim: int, emb_dim: int, layers: int = 2, seed: int = 42):
        self.ws = [randn((in_dim if i == 0 else emb_dim) * 2, emb_dim, seed=seed + i) for i in range(layers)]

    def __call__(self, x: Matrix, edge_index: EdgeIndex) -> Matrix:
        h = x
        adj = edge_index_to_adj(edge_index, len(h))
        for w in self.ws:
            neigh = matmul(adj, h)
            h = relu(matmul(concat(h, neigh), w))
        return h


class GATEncoder:
    def __init__(self, in_dim: int, emb_dim: int, seed: int = 42):
        self.wq = randn(in_dim, emb_dim, seed=seed)
        self.wk = randn(in_dim, emb_dim, seed=seed + 1)
        self.wv = randn(in_dim, emb_dim, seed=seed + 2)

    def __call__(self, x: Matrix, edge_index: EdgeIndex) -> Matrix:
        q, k, v = matmul(x, self.wq), matmul(x, self.wk), matmul(x, self.wv)
        n = len(x)
        neigh = [[0] * n for _ in range(n)]
        for s, d in edge_index:
            neigh[s][d] = 1
        for i in range(n):
            neigh[i][i] = 1

        out = []
        for i in range(n):
            logits = []
            for j in range(n):
                if neigh[i][j] == 1:
                    logits.append(sum(a * b for a, b in zip(q[i], k[j])) / (len(q[i]) ** 0.5))
                else:
                    logits.append(-1e9)
            attn = softmax(logits)
            out.append([sum(attn[j] * v[j][d] for j in range(n)) for d in range(len(v[0]))])
        return out

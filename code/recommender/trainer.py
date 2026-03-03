from __future__ import annotations

import os
import random
from dataclasses import dataclass
from typing import Dict, List

from .evaluate import EvalResult, evaluate_topk
from .interfaces import GraphBatch, Interactions


@dataclass
class EpochLog:
    epoch: int
    total_loss: float
    rec_error: float
    cl_error: float
    uniform_error: float
    reg_error: float
    recall_at_20: float
    ndcg_at_20: float


class RecommenderTrainer:
    """Trainable runner with SGD over node features + full loss monitoring."""

    def __init__(self, model, lr: float = 0.05, seed: int = 42):
        self.model = model
        self.lr = lr
        self.rng = random.Random(seed)

    def _bpr_sgd_update(self, graph: GraphBatch, triplets: Dict[str, List[int]]):
        # Lightweight SGD on node features for direct trainability.
        for u, p, n in zip(triplets["users"], triplets["pos_items"], triplets["neg_items"]):
            u_vec = graph.x[u]
            p_vec = graph.x[p]
            n_vec = graph.x[n]
            x_uij = sum(a * (b - c) for a, b, c in zip(u_vec, p_vec, n_vec))
            coeff = 1.0 / (1.0 + pow(2.718281828, x_uij))

            for d in range(len(u_vec)):
                grad_u = coeff * (p_vec[d] - n_vec[d])
                grad_p = coeff * u_vec[d]
                grad_n = -coeff * u_vec[d]
                graph.x[u][d] += self.lr * grad_u
                graph.x[p][d] += self.lr * grad_p
                graph.x[n][d] += self.lr * grad_n

    def fit(
        self,
        graph: GraphBatch,
        train_interactions: Interactions,
        test_interactions: Interactions,
        item_pool: List[int],
        epochs: int = 20,
        batch_size: int = 2048,
    ) -> List[EpochLog]:
        logs: List[EpochLog] = []
        for epoch in range(1, epochs + 1):
            triplets = self.model.pos_neg_sampler.sample(train_interactions, item_pool, batch_size)
            self._bpr_sgd_update(graph, triplets)

            out = self.model.forward(
                graph=graph,
                interactions=train_interactions,
                item_pool=item_pool,
                batch_size=batch_size,
            )
            z = self.model.encoder(graph.x, graph.edge_index)
            num_users = len(train_interactions)
            user_emb = z[:num_users]
            item_emb = z[num_users:]

            eval_out: EvalResult = evaluate_topk(
                user_emb=user_emb,
                item_emb=item_emb,
                train_interactions={u: [i - num_users for i in items] for u, items in train_interactions.items()},
                test_interactions={u: [i - num_users for i in items] for u, items in test_interactions.items()},
                k=20,
            )

            row = EpochLog(
                epoch=epoch,
                total_loss=out.loss,
                rec_error=out.rec_error,
                cl_error=out.cl_error,
                uniform_error=out.uniform_error,
                reg_error=out.reg_error,
                recall_at_20=eval_out.recall_at_k,
                ndcg_at_20=eval_out.ndcg_at_k,
            )
            logs.append(row)
            print(
                f"[Epoch {epoch:03d}] total={row.total_loss:.4f} rec={row.rec_error:.4f} cl={row.cl_error:.4f} "
                f"uniform={row.uniform_error:.4f} reg={row.reg_error:.6f} R@20={row.recall_at_20:.4f} NDCG@20={row.ndcg_at_20:.4f}"
            )
        return logs


def save_training_curve(logs: List[EpochLog], output_dir: str = "artifacts"):
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "training_curve.csv")
    txt_path = os.path.join(output_dir, "training_curve.txt")

    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("epoch,total_loss,rec_error,cl_error,uniform_error,reg_error,recall_at_20,ndcg_at_20\n")
        for x in logs:
            f.write(
                f"{x.epoch},{x.total_loss:.6f},{x.rec_error:.6f},{x.cl_error:.6f},{x.uniform_error:.6f},"
                f"{x.reg_error:.6f},{x.recall_at_20:.6f},{x.ndcg_at_20:.6f}\n"
            )

    # Console-friendly visualization (ASCII bars)
    losses = [x.total_loss for x in logs]
    lo, hi = min(losses), max(losses)
    span = max(hi - lo, 1e-8)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("ASCII Training Curve (total_loss)\n")
        for x in logs:
            n = int((x.total_loss - lo) / span * 40)
            f.write(f"epoch {x.epoch:03d} | {'█' * n}\n")

    print(f"训练曲线已保存: {csv_path}")
    print(f"ASCII可视化已保存: {txt_path}")

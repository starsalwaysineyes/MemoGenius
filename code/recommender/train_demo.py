from __future__ import annotations

import random

from recommender import (
    GraphBatch,
    GraphSAGEEncoder,
    HybridCLStrategy,
    InfoNCEContrastiveLoss,
    ModularGCLRecommender,
    ObjectiveWeights,
    PopularityNegativeSampler,
)
from recommender.trainer import RecommenderTrainer, save_training_curve


def synthetic_graph(num_users: int = 8, num_items: int = 12, feat_dim: int = 16, seed: int = 42) -> GraphBatch:
    rng = random.Random(seed)
    num_nodes = num_users + num_items
    x = [[rng.gauss(0, 1) for _ in range(feat_dim)] for _ in range(num_nodes)]

    edges = []
    for u in range(num_users):
        for _ in range(3):
            i = rng.randint(num_users, num_nodes - 1)
            edges.append((u, i))
            edges.append((i, u))
    return GraphBatch(x=x, edge_index=edges)


def synthetic_interactions(num_users: int = 8, num_items: int = 12, min_pos: int = 2, max_pos: int = 4, seed: int = 42):
    rng = random.Random(seed)
    interactions = {}
    for u in range(num_users):
        k = rng.randint(min_pos, max_pos)
        interactions[u] = [num_users + i for i in rng.sample(range(num_items), k=k)]
    return interactions


def split_train_test(interactions):
    train, test = {}, {}
    for u, items in interactions.items():
        train[u] = items[1:]
        test[u] = items[:1]
    return train, test


def main():
    num_users, num_items = 8, 12
    graph = synthetic_graph(num_users=num_users, num_items=num_items)
    interactions = synthetic_interactions(num_users=num_users, num_items=num_items)
    train_interactions, test_interactions = split_train_test(interactions)

    model = ModularGCLRecommender(
        encoder=GraphSAGEEncoder(in_dim=16, emb_dim=32),
        pos_neg_sampler=PopularityNegativeSampler(),
        graph_cl_strategy=HybridCLStrategy(drop_rate=0.2, mask_rate=0.2),
        contrastive_loss=InfoNCEContrastiveLoss(temperature=0.2),
        weights=ObjectiveWeights(rec=1.0, cl=0.2, uniform=0.05, reg=1e-4),
    )

    trainer = RecommenderTrainer(model=model, lr=0.03)
    item_pool = list(range(num_users, num_users + num_items))
    logs = trainer.fit(
        graph=graph,
        train_interactions=train_interactions,
        test_interactions=test_interactions,
        item_pool=item_pool,
        epochs=5,
        batch_size=64,
    )
    save_training_curve(logs)


if __name__ == "__main__":
    main()

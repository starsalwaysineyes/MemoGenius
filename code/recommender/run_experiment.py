from __future__ import annotations

import argparse
import random

from recommender import (
    EdgeDropCLStrategy,
    GATEncoder,
    GraphBatch,
    GraphSAGEEncoder,
    HybridCLStrategy,
    InfoNCEContrastiveLoss,
    LightGCNEncoder,
    ModularGCLRecommender,
    NodeDropCLStrategy,
    ObjectiveWeights,
    PopularityNegativeSampler,
    UniformUserPosNegSampler,
    HardNegativeSampler,
)
from recommender.data import (
    DatasetBundle,
    load_amazon_book_from_txt,
    load_gowalla_from_txt,
    load_movielens_100k,
    load_yelp2018_from_txt,
)
from recommender.trainer import RecommenderTrainer, save_training_curve


def _build_bipartite_graph(bundle: DatasetBundle, feat_dim: int = 32, seed: int = 42):
    rng = random.Random(seed)
    total_nodes = bundle.num_users + bundle.num_items
    x = [[rng.gauss(0, 0.1) for _ in range(feat_dim)] for _ in range(total_nodes)]

    edge_index = []
    for u, items in bundle.train_interactions.items():
        for i in items:
            item_node = bundle.num_users + i
            edge_index.append((u, item_node))
            edge_index.append((item_node, u))
    return GraphBatch(x=x, edge_index=edge_index)


def _shift_interactions(bundle: DatasetBundle):
    # Shift item id to global node id in graph (user nodes first, then item nodes).
    train = {u: [bundle.num_users + i for i in items] for u, items in bundle.train_interactions.items()}
    test = {u: [bundle.num_users + i for i in items] for u, items in bundle.test_interactions.items()}
    return train, test


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", choices=["ml100k", "gowalla", "yelp2018", "amazon-book"], default="ml100k")
    p.add_argument("--dataset_path", default="", help="for gowalla/yelp2018/amazon-book txt path")
    p.add_argument("--encoder", choices=["lightgcn", "graphsage", "gat"], default="graphsage")
    p.add_argument("--sampler", choices=["uniform", "popularity", "hard"], default="popularity")
    p.add_argument("--cl", choices=["edge", "node", "hybrid"], default="hybrid")
    p.add_argument("--epochs", type=int, default=10)
    p.add_argument("--batch_size", type=int, default=512)
    args = p.parse_args()

    if args.dataset == "ml100k":
        bundle = load_movielens_100k()
    elif args.dataset == "gowalla":
        bundle = load_gowalla_from_txt(args.dataset_path)
    elif args.dataset == "yelp2018":
        bundle = load_yelp2018_from_txt(args.dataset_path)
    else:
        bundle = load_amazon_book_from_txt(args.dataset_path)

    graph = _build_bipartite_graph(bundle)
    train_interactions, test_interactions = _shift_interactions(bundle)

    if args.encoder == "lightgcn":
        encoder = LightGCNEncoder(in_dim=32, emb_dim=32)
    elif args.encoder == "gat":
        encoder = GATEncoder(in_dim=32, emb_dim=32)
    else:
        encoder = GraphSAGEEncoder(in_dim=32, emb_dim=32)

    if args.sampler == "uniform":
        pos_neg_sampler = UniformUserPosNegSampler()
    elif args.sampler == "hard":
        pos_neg_sampler = HardNegativeSampler(top_k=100)
    else:
        pos_neg_sampler = PopularityNegativeSampler()

    if args.cl == "edge":
        cl_strategy = EdgeDropCLStrategy(drop_rate_a=0.2, drop_rate_b=0.3)
    elif args.cl == "node":
        cl_strategy = NodeDropCLStrategy(keep_rate_a=0.9, keep_rate_b=0.8)
    else:
        cl_strategy = HybridCLStrategy(drop_rate=0.2, mask_rate=0.2)

    model = ModularGCLRecommender(
        encoder=encoder,
        pos_neg_sampler=pos_neg_sampler,
        graph_cl_strategy=cl_strategy,
        contrastive_loss=InfoNCEContrastiveLoss(temperature=0.2),
        weights=ObjectiveWeights(rec=1.0, cl=0.2, uniform=0.05, reg=1e-4),
    )

    trainer = RecommenderTrainer(model=model, lr=0.03)
    item_pool = list(range(bundle.num_users, bundle.num_users + bundle.num_items))
    logs = trainer.fit(
        graph=graph,
        train_interactions=train_interactions,
        test_interactions=test_interactions,
        item_pool=item_pool,
        epochs=args.epochs,
        batch_size=args.batch_size,
    )
    save_training_curve(logs)


if __name__ == "__main__":
    main()

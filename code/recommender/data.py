from __future__ import annotations

import os
import random
import urllib.request
import zipfile
from dataclasses import dataclass
from typing import Dict, List, Tuple

Interactions = Dict[int, List[int]]


@dataclass
class DatasetBundle:
    name: str
    num_users: int
    num_items: int
    train_interactions: Interactions
    test_interactions: Interactions


def _split_train_test(interactions: Interactions, seed: int = 42) -> Tuple[Interactions, Interactions]:
    rng = random.Random(seed)
    train, test = {}, {}
    for u, items in interactions.items():
        unique = sorted(set(items))
        if len(unique) <= 1:
            train[u], test[u] = unique, []
            continue
        rng.shuffle(unique)
        test[u] = [unique[0]]
        train[u] = unique[1:]
    return train, test


def _build_from_pairs(name: str, pairs: List[Tuple[int, int]], user_base: int = 0, item_base: int = 0) -> DatasetBundle:
    user_map, item_map = {}, {}
    interactions: Interactions = {}
    for u_raw, i_raw in pairs:
        if u_raw not in user_map:
            user_map[u_raw] = len(user_map)
        if i_raw not in item_map:
            item_map[i_raw] = len(item_map)
        u, i = user_map[u_raw], item_map[i_raw]
        interactions.setdefault(u, []).append(i)
    train, test = _split_train_test(interactions)
    return DatasetBundle(
        name=name,
        num_users=len(user_map),
        num_items=len(item_map),
        train_interactions=train,
        test_interactions=test,
    )


def load_movielens_100k(root: str = "code/recommender/datasets") -> DatasetBundle:
    os.makedirs(root, exist_ok=True)
    zip_path = os.path.join(root, "ml-100k.zip")
    data_dir = os.path.join(root, "ml-100k")
    file_path = os.path.join(data_dir, "u.data")

    if not os.path.exists(file_path):
        try:
            if not os.path.exists(zip_path):
                urllib.request.urlretrieve("https://files.grouplens.org/datasets/movielens/ml-100k.zip", zip_path)
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(root)
        except Exception:
            # Network-constrained fallback mini-dataset
            pairs = [
                (1, 10), (1, 11), (1, 12),
                (2, 10), (2, 13),
                (3, 11), (3, 14),
                (4, 12), (4, 13), (4, 14),
                (5, 10), (5, 14),
            ]
            return _build_from_pairs("movielens-100k-fallback", pairs)

    pairs = []
    with open(file_path, "r", encoding="latin-1") as f:
        for line in f:
            user, item, rating, _ts = line.strip().split("\t")
            if float(rating) >= 4.0:
                pairs.append((int(user), int(item)))
    return _build_from_pairs("movielens-100k", pairs)


def load_gowalla_from_txt(path: str) -> DatasetBundle:
    # Common recommendation format: each line 'user item1 item2 ...'
    pairs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            arr = line.strip().split()
            if len(arr) <= 1:
                continue
            u = int(arr[0])
            for item in arr[1:]:
                pairs.append((u, int(item)))
    return _build_from_pairs("gowalla", pairs)


def load_yelp2018_from_txt(path: str) -> DatasetBundle:
    pairs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            arr = line.strip().split()
            if len(arr) <= 1:
                continue
            u = int(arr[0])
            for item in arr[1:]:
                pairs.append((u, int(item)))
    return _build_from_pairs("yelp2018", pairs)


def load_amazon_book_from_txt(path: str) -> DatasetBundle:
    pairs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            arr = line.strip().split()
            if len(arr) <= 1:
                continue
            u = int(arr[0])
            for item in arr[1:]:
                pairs.append((u, int(item)))
    return _build_from_pairs("amazon-book", pairs)

from __future__ import annotations

import random
from collections import Counter

from .interfaces import Interactions, PositiveNegativeSampler, Triplets


class UniformUserPosNegSampler(PositiveNegativeSampler):
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

    def sample(self, interactions: Interactions, item_pool, batch_size: int) -> Triplets:
        users = list(interactions.keys())
        out_users, pos_items, neg_items = [], [], []
        for _ in range(batch_size):
            u = self.rng.choice(users)
            pos = self.rng.choice(interactions[u])
            user_pos_set = set(interactions[u])
            neg = self.rng.choice(item_pool)
            while neg in user_pos_set:
                neg = self.rng.choice(item_pool)
            out_users.append(u)
            pos_items.append(pos)
            neg_items.append(neg)
        return {"users": out_users, "pos_items": pos_items, "neg_items": neg_items}


class PopularityNegativeSampler(PositiveNegativeSampler):
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

    def sample(self, interactions: Interactions, item_pool, batch_size: int) -> Triplets:
        item_counter = Counter()
        for items in interactions.values():
            item_counter.update(items)
        weights = [item_counter.get(i, 1) for i in item_pool]

        users = list(interactions.keys())
        out_users, pos_items, neg_items = [], [], []
        for _ in range(batch_size):
            u = self.rng.choice(users)
            pos = self.rng.choice(interactions[u])
            user_pos_set = set(interactions[u])
            neg = self.rng.choices(item_pool, weights=weights, k=1)[0]
            while neg in user_pos_set:
                neg = self.rng.choices(item_pool, weights=weights, k=1)[0]
            out_users.append(u)
            pos_items.append(pos)
            neg_items.append(neg)
        return {"users": out_users, "pos_items": pos_items, "neg_items": neg_items}


class HardNegativeSampler(PositiveNegativeSampler):
    def __init__(self, top_k: int = 20, seed: int = 42):
        self.top_k = top_k
        self.rng = random.Random(seed)

    def sample(self, interactions: Interactions, item_pool, batch_size: int) -> Triplets:
        item_counter = Counter()
        for items in interactions.values():
            item_counter.update(items)
        sorted_items = [i for i, _ in item_counter.most_common()] + [i for i in item_pool if i not in item_counter]
        hard_pool = sorted_items[: max(1, min(self.top_k, len(item_pool)))]

        users = list(interactions.keys())
        out_users, pos_items, neg_items = [], [], []
        for _ in range(batch_size):
            u = self.rng.choice(users)
            pos = self.rng.choice(interactions[u])
            user_pos_set = set(interactions[u])
            candidates = [i for i in hard_pool if i not in user_pos_set]
            if not candidates:
                candidates = [i for i in item_pool if i not in user_pos_set]
            neg = self.rng.choice(candidates)
            out_users.append(u)
            pos_items.append(pos)
            neg_items.append(neg)
        return {"users": out_users, "pos_items": pos_items, "neg_items": neg_items}

from __future__ import annotations

from dataclasses import dataclass

from .interfaces import GraphBatch, Interactions, PositiveNegativeSampler, gather_triplets
from .objective import (
    LossBreakdown,
    ObjectiveWeights,
    bpr_recommendation_error,
    l2_regularization_error,
    node_uniformity_error,
)


@dataclass
class TrainingOutput:
    loss: float
    rec_error: float
    cl_error: float
    uniform_error: float
    reg_error: float


class ModularGCLRecommender:
    """Decoupled framework:
    1) pluggable GNN encoder
    2) pluggable positive/negative sampler
    3) pluggable graph CL view strategy
    Fixed loss = rec + cl + uniform + reg (with coefficients)
    """

    def __init__(
        self,
        encoder,
        pos_neg_sampler: PositiveNegativeSampler,
        graph_cl_strategy,
        contrastive_loss,
        weights: ObjectiveWeights | None = None,
    ):
        self.encoder = encoder
        self.pos_neg_sampler = pos_neg_sampler
        self.graph_cl_strategy = graph_cl_strategy
        self.contrastive_loss = contrastive_loss
        self.weights = weights or ObjectiveWeights()

    def forward(self, graph: GraphBatch, interactions: Interactions, item_pool, batch_size: int) -> TrainingOutput:
        z = self.encoder(graph.x, graph.edge_index)

        triplets = self.pos_neg_sampler.sample(interactions, item_pool=item_pool, batch_size=batch_size)
        user_emb, pos_emb, neg_emb = gather_triplets(z, triplets)
        rec_error = bpr_recommendation_error(user_emb, pos_emb, neg_emb)

        g1, g2 = self.graph_cl_strategy.generate(graph)
        z1 = self.encoder(g1.x, g1.edge_index)
        z2 = self.encoder(g2.x, g2.edge_index)
        min_nodes = min(len(z1), len(z2))
        cl_error = self.contrastive_loss.compute(z1[:min_nodes], z2[:min_nodes])

        uniform_error = node_uniformity_error(z)
        reg_error = l2_regularization_error(z)

        total = (
            self.weights.rec * rec_error
            + self.weights.cl * cl_error
            + self.weights.uniform * uniform_error
            + self.weights.reg * reg_error
        )
        return TrainingOutput(
            loss=total,
            rec_error=rec_error,
            cl_error=cl_error,
            uniform_error=uniform_error,
            reg_error=reg_error,
        )

    def breakdown(self, graph: GraphBatch, interactions: Interactions, item_pool, batch_size: int) -> LossBreakdown:
        out = self.forward(graph, interactions, item_pool, batch_size)
        return LossBreakdown(
            total=out.loss,
            rec_error=out.rec_error,
            cl_error=out.cl_error,
            uniform_error=out.uniform_error,
            reg_error=out.reg_error,
        )

"""
AI Tanács - Voting Mechanisms
Implements Borda Count, IRV, MRR and hybrid voting
"""
from typing import List, Dict, Tuple
from collections import defaultdict, Counter


class VotingSystem:
    """Implements various voting mechanisms for AI Council"""

    @staticmethod
    def borda_count(
        responses: List[Dict],
        weights: Dict[str, float] = None
    ) -> Tuple[str, Dict[str, float]]:
        """
        Weighted Borda Count voting

        Args:
            responses: List of agent responses with scores
            weights: Optional per-agent weights (default: 1.0 for all)

        Returns:
            (winner_text, scores_dict)
        """
        if not responses:
            return "", {}

        weights = weights or {}
        scores = defaultdict(float)

        # Calculate weighted Borda scores
        n = len(responses)
        for i, response in enumerate(responses):
            agent_name = response.get("agent", "Unknown")
            text = response.get("text", "")
            base_score = response.get("score", 5.0)
            weight = weights.get(agent_name, 1.0)

            # Borda points: (n - position) * weight * base_score
            borda_points = (n - i) * weight * base_score
            scores[text] = scores.get(text, 0) + borda_points

        # Find winner
        winner = max(scores.items(), key=lambda x: x[1])
        return winner[0], dict(scores)

    @staticmethod
    def instant_runoff(
        responses: List[Dict],
        weights: Dict[str, float] = None
    ) -> Tuple[str, Dict[str, float]]:
        """
        Instant Runoff Voting (IRV)

        Eliminates lowest-scoring responses until one has >50%
        """
        if not responses:
            return "", {}

        weights = weights or {}
        candidates = {r["text"]: 0.0 for r in responses}

        # Initial weighted votes
        for response in responses:
            text = response["text"]
            weight = weights.get(response.get("agent", "Unknown"), 1.0)
            base_score = response.get("score", 5.0)
            candidates[text] += weight * base_score

        total_votes = sum(candidates.values())

        # IRV elimination rounds
        while len(candidates) > 1:
            # Check if any candidate has >50%
            for text, votes in candidates.items():
                if votes / total_votes > 0.5:
                    return text, candidates

            # Eliminate lowest scorer
            min_text = min(candidates.items(), key=lambda x: x[1])[0]
            del candidates[min_text]
            total_votes = sum(candidates.values())

        # Return last standing
        winner_text = list(candidates.keys())[0] if candidates else ""
        return winner_text, candidates

    @staticmethod
    def mean_reciprocal_rank(
        responses: List[Dict],
        weights: Dict[str, float] = None
    ) -> Tuple[str, Dict[str, float]]:
        """
        Mean Reciprocal Rank (MRR)

        Emphasizes top-ranked responses
        """
        if not responses:
            return "", {}

        weights = weights or {}
        scores = defaultdict(float)

        for rank, response in enumerate(responses, start=1):
            text = response["text"]
            agent_name = response.get("agent", "Unknown")
            weight = weights.get(agent_name, 1.0)
            base_score = response.get("score", 5.0)

            # MRR score: weight * base_score / rank
            mrr_score = (weight * base_score) / rank
            scores[text] += mrr_score

        winner = max(scores.items(), key=lambda x: x[1])
        return winner[0], dict(scores)

    @staticmethod
    def hybrid_vote(
        responses: List[Dict],
        weights: Dict[str, float] = None
    ) -> Tuple[str, Dict[str, float]]:
        """
        Hybrid voting: 40% Borda + 40% MRR + 20% IRV

        Balances consensus and quality
        """
        if not responses:
            return "", {}

        # Get results from each method
        borda_winner, borda_scores = VotingSystem.borda_count(responses, weights)
        mrr_winner, mrr_scores = VotingSystem.mean_reciprocal_rank(responses, weights)
        irv_winner, irv_scores = VotingSystem.instant_runoff(responses, weights)

        # Normalize scores to 0-1 range for each method
        def normalize(scores_dict):
            if not scores_dict:
                return {}
            max_score = max(scores_dict.values())
            if max_score == 0:
                return scores_dict
            return {k: v / max_score for k, v in scores_dict.items()}

        borda_norm = normalize(borda_scores)
        mrr_norm = normalize(mrr_scores)
        irv_norm = normalize(irv_scores)

        # Combine with weights: 40% Borda + 40% MRR + 20% IRV
        combined = defaultdict(float)
        all_texts = set(borda_norm.keys()) | set(mrr_norm.keys()) | set(irv_norm.keys())

        for text in all_texts:
            combined[text] = (
                0.4 * borda_norm.get(text, 0) +
                0.4 * mrr_norm.get(text, 0) +
                0.2 * irv_norm.get(text, 0)
            )

        winner = max(combined.items(), key=lambda x: x[1])
        return winner[0], dict(combined)


def get_voting_system(method: str = "borda"):
    """
    Factory function to get voting method

    Args:
        method: One of 'borda', 'irv', 'mrr', 'hybrid'

    Returns:
        Voting function
    """
    methods = {
        "borda": VotingSystem.borda_count,
        "irv": VotingSystem.instant_runoff,
        "mrr": VotingSystem.mean_reciprocal_rank,
        "hybrid": VotingSystem.hybrid_vote,
    }
    return methods.get(method, VotingSystem.borda_count)

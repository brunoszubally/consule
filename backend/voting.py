"""
AI Tanács - Voting Mechanisms
Implements Borda Count, IRV, MRR and hybrid voting
"""
from typing import List, Dict, Tuple, Any
from collections import defaultdict, Counter


class VotingSystem:
    """Implements various voting mechanisms for AI Council"""

    @staticmethod
    def borda_count(
        responses: List[Dict],
        weights: Dict[str, float] = None
    ) -> Tuple[str, Dict[str, float], Dict[str, Any]]:
        """
        Weighted Borda Count voting

        Args:
            responses: List of agent responses with scores
            weights: Optional per-agent weights (default: 1.0 for all)

        Returns:
            (winner_text, scores_dict, details_dict)
        """
        if not responses:
            return "", {}, {}

        weights = weights or {}
        scores = defaultdict(float)
        details = {
            "method": "Borda Count",
            "calculations": [],
            "total_agents": len(responses)
        }

        # Calculate weighted Borda scores
        n = len(responses)
        for i, response in enumerate(responses):
            agent_name = response.get("agent", "Unknown")
            text = response.get("text", "")
            base_score = response.get("score", 5.0)
            weight = weights.get(agent_name, 1.0)

            # Borda points: (n - position) * weight * base_score
            position_points = n - i
            borda_points = position_points * weight * base_score
            scores[text] = scores.get(text, 0) + borda_points

            # Store calculation details
            details["calculations"].append({
                "agent": agent_name,
                "position": i + 1,
                "position_points": position_points,
                "base_score": base_score,
                "weight": weight,
                "borda_points": borda_points,
                "formula": f"({n} - {i}) × {weight} × {base_score} = {borda_points}"
            })

        # Find winner
        winner = max(scores.items(), key=lambda x: x[1])
        return winner[0], dict(scores), details

    @staticmethod
    def instant_runoff(
        responses: List[Dict],
        weights: Dict[str, float] = None
    ) -> Tuple[str, Dict[str, float], Dict[str, Any]]:
        """
        Instant Runoff Voting (IRV)

        Eliminates lowest-scoring responses until one has >50%
        """
        if not responses:
            return "", {}, {}

        weights = weights or {}
        candidates = {r["text"]: 0.0 for r in responses}
        details = {
            "method": "Instant Runoff Voting (IRV)",
            "rounds": [],
            "eliminations": []
        }

        # Initial weighted votes
        for response in responses:
            text = response["text"]
            agent_name = response.get("agent", "Unknown")
            weight = weights.get(agent_name, 1.0)
            base_score = response.get("score", 5.0)
            candidates[text] += weight * base_score

        total_votes = sum(candidates.values())

        # IRV elimination rounds
        round_num = 1
        while len(candidates) > 1:
            # Record current round state
            round_data = {
                "round": round_num,
                "candidates": dict(candidates),
                "total_votes": total_votes
            }

            # Check if any candidate has >50%
            for text, votes in candidates.items():
                percentage = (votes / total_votes * 100) if total_votes > 0 else 0
                if votes / total_votes > 0.5:
                    round_data["winner"] = text
                    round_data["winner_percentage"] = percentage
                    details["rounds"].append(round_data)
                    return text, candidates, details

            # Eliminate lowest scorer
            min_item = min(candidates.items(), key=lambda x: x[1])
            min_text = min_item[0]
            min_votes = min_item[1]

            details["eliminations"].append({
                "round": round_num,
                "eliminated": min_text[:50] + "..." if len(min_text) > 50 else min_text,
                "votes": min_votes
            })

            del candidates[min_text]
            total_votes = sum(candidates.values())

            details["rounds"].append(round_data)
            round_num += 1

        # Return last standing
        winner_text = list(candidates.keys())[0] if candidates else ""
        details["final_winner"] = winner_text[:50] + "..." if len(winner_text) > 50 else winner_text
        return winner_text, candidates, details

    @staticmethod
    def mean_reciprocal_rank(
        responses: List[Dict],
        weights: Dict[str, float] = None
    ) -> Tuple[str, Dict[str, float], Dict[str, Any]]:
        """
        Mean Reciprocal Rank (MRR)

        Emphasizes top-ranked responses
        """
        if not responses:
            return "", {}, {}

        weights = weights or {}
        scores = defaultdict(float)
        details = {
            "method": "Mean Reciprocal Rank (MRR)",
            "calculations": []
        }

        for rank, response in enumerate(responses, start=1):
            text = response["text"]
            agent_name = response.get("agent", "Unknown")
            weight = weights.get(agent_name, 1.0)
            base_score = response.get("score", 5.0)

            # MRR score: weight * base_score / rank
            mrr_score = (weight * base_score) / rank
            scores[text] += mrr_score

            details["calculations"].append({
                "agent": agent_name,
                "rank": rank,
                "base_score": base_score,
                "weight": weight,
                "mrr_score": mrr_score,
                "formula": f"({weight} × {base_score}) / {rank} = {mrr_score:.3f}"
            })

        winner = max(scores.items(), key=lambda x: x[1])
        return winner[0], dict(scores), details

    @staticmethod
    def hybrid_vote(
        responses: List[Dict],
        weights: Dict[str, float] = None
    ) -> Tuple[str, Dict[str, float], Dict[str, Any]]:
        """
        Hybrid voting: 40% Borda + 40% MRR + 20% IRV

        Balances consensus and quality
        """
        if not responses:
            return "", {}, {}

        # Get results from each method
        borda_winner, borda_scores, borda_details = VotingSystem.borda_count(responses, weights)
        mrr_winner, mrr_scores, mrr_details = VotingSystem.mean_reciprocal_rank(responses, weights)
        irv_winner, irv_scores, irv_details = VotingSystem.instant_runoff(responses, weights)

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

        # Detailed breakdown
        details = {
            "method": "Hybrid Vote (40% Borda + 40% MRR + 20% IRV)",
            "component_winners": {
                "borda": borda_winner[:50] + "..." if len(borda_winner) > 50 else borda_winner,
                "mrr": mrr_winner[:50] + "..." if len(mrr_winner) > 50 else mrr_winner,
                "irv": irv_winner[:50] + "..." if len(irv_winner) > 50 else irv_winner
            },
            "normalized_scores": {
                "borda": dict(borda_norm),
                "mrr": dict(mrr_norm),
                "irv": dict(irv_norm)
            },
            "component_details": {
                "borda": borda_details,
                "mrr": mrr_details,
                "irv": irv_details
            }
        }

        return winner[0], dict(combined), details


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

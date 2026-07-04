"""
Self-Consistency pattern: sample multiple reasoning paths and take majority vote.
"""

from collections import Counter

from prompt_engineering.config.settings import get_settings
from prompt_engineering.utils.logger import get_logger

logger = get_logger(__name__)


class SelfConsistencyPattern:
    """Generates multiple answers and selects by majority vote."""

    def __init__(self) -> None:
        self._settings = get_settings()

    def majority_vote(self, answers: list[str]) -> dict:
        """
        Select the most common answer from multiple samples.

        Args:
            answers: List of answers from multiple LLM calls.

        Returns:
            Dict with 'answer', 'confidence', and 'vote_counts'.
        """
        if not answers:
            return {"answer": "", "confidence": 0.0, "vote_counts": {}}

        # Normalize answers for comparison
        normalized = [a.strip().lower() for a in answers]
        counter = Counter(normalized)
        winner, count = counter.most_common(1)[0]

        # Find original (non-normalized) version of winner
        original = next(a for a in answers if a.strip().lower() == winner)
        confidence = count / len(answers)

        logger.info("majority_vote", winner=winner[:50], confidence=confidence, total=len(answers))

        return {
            "answer": original,
            "confidence": confidence,
            "vote_counts": dict(counter),
            "total_samples": len(answers),
            "agreement": count,
        }

    def get_num_samples(self) -> int:
        """Get configured number of samples for self-consistency."""
        return self._settings.patterns.self_consistency_samples

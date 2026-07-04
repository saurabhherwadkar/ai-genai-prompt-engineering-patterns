"""A/B testing framework for comparing prompt variants."""

import math

from prompt_engineering.config.settings import get_settings
from prompt_engineering.models.schemas import ABTestResult
from prompt_engineering.utils.logger import get_logger

logger = get_logger(__name__)


class ABTester:
    """Compares two prompt variants using statistical testing."""

    def __init__(self) -> None:
        self._settings = get_settings()

    def compare(self, scores_a: list[float], scores_b: list[float], name_a: str = "A", name_b: str = "B") -> ABTestResult:
        """
        Compare two sets of quality scores and determine a winner.

        Uses simple z-test for difference in means.

        Args:
            scores_a: Quality scores for prompt A.
            scores_b: Quality scores for prompt B.
            name_a: Name of prompt A.
            name_b: Name of prompt B.

        Returns:
            ABTestResult with winner and significance.
        """
        n_a, n_b = len(scores_a), len(scores_b)
        if not n_a or not n_b:
            return ABTestResult(prompt_a=name_a, prompt_b=name_b, winner="inconclusive", num_samples=0)

        mean_a = sum(scores_a) / n_a
        mean_b = sum(scores_b) / n_b

        # Determine winner by mean score
        winner = name_a if mean_a >= mean_b else name_b

        # Calculate significance (simplified z-test)
        var_a = sum((x - mean_a) ** 2 for x in scores_a) / max(n_a - 1, 1)
        var_b = sum((x - mean_b) ** 2 for x in scores_b) / max(n_b - 1, 1)
        se = math.sqrt(var_a / n_a + var_b / n_b) if (var_a + var_b) > 0 else 1.0
        z_score = abs(mean_a - mean_b) / se if se > 0 else 0

        # Approximate significance (z > 1.96 = p < 0.05)
        significant = z_score > 1.96 and min(n_a, n_b) >= self._settings.testing.ab_test_min_samples

        confidence = min(1.0, z_score / 3.0)  # Normalized confidence

        logger.info("ab_test_complete", winner=winner, mean_a=round(mean_a, 3), mean_b=round(mean_b, 3), significant=significant)

        return ABTestResult(
            prompt_a=name_a, prompt_b=name_b, winner=winner,
            a_score=round(mean_a, 3), b_score=round(mean_b, 3),
            num_samples=n_a + n_b, confidence=round(confidence, 3), significant=significant,
        )

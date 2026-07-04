"""Prompt regression testing: ensure prompt changes don't degrade quality."""

from prompt_engineering.models.schemas import TestCase, TestResult
from prompt_engineering.utils.logger import get_logger

logger = get_logger(__name__)


class PromptRegressionTester:
    """Runs test cases against a prompt to detect regressions."""

    def run_test(self, test_case: TestCase, output: str) -> TestResult:
        """
        Evaluate a single test case against LLM output.

        Args:
            test_case: The test case with expectations.
            output: The LLM output to evaluate.

        Returns:
            TestResult with pass/fail and reasoning.
        """
        # Check expected_contains
        for expected in test_case.expected_contains:
            if expected.lower() not in output.lower():
                return TestResult(
                    test_id=test_case.test_id, passed=False, output=output,
                    reason=f"Missing expected content: '{expected}'",
                )

        # Check expected_not_contains
        for forbidden in test_case.expected_not_contains:
            if forbidden.lower() in output.lower():
                return TestResult(
                    test_id=test_case.test_id, passed=False, output=output,
                    reason=f"Contains forbidden content: '{forbidden}'",
                )

        return TestResult(test_id=test_case.test_id, passed=True, output=output, score=1.0, reason="All checks passed")

    def run_suite(self, test_cases: list[TestCase], outputs: list[str]) -> dict:
        """
        Run a full test suite.

        Args:
            test_cases: List of test cases.
            outputs: Corresponding LLM outputs.

        Returns:
            Summary with pass rate and results.
        """
        results = []
        for tc, output in zip(test_cases, outputs):
            results.append(self.run_test(tc, output))

        passed = sum(1 for r in results if r.passed)
        total = len(results)
        pass_rate = passed / total if total > 0 else 0

        logger.info("regression_suite_complete", passed=passed, total=total, pass_rate=pass_rate)
        return {"pass_rate": pass_rate, "passed": passed, "total": total, "results": results}

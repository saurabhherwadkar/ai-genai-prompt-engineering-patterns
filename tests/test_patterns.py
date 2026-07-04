"""Tests for prompt patterns and testing framework."""
import pytest
from prompt_engineering.patterns.chain_of_thought import ChainOfThoughtPattern
from prompt_engineering.patterns.few_shot import FewShotPattern
from prompt_engineering.patterns.self_consistency import SelfConsistencyPattern
from prompt_engineering.testing.regression import PromptRegressionTester
from prompt_engineering.testing.ab_test import ABTester
from prompt_engineering.models.schemas import TestCase


class TestChainOfThought:
    def test_zero_shot_cot(self) -> None:
        cot = ChainOfThoughtPattern()
        result = cot.apply("What is 2+2?")
        assert "step by step" in result.lower()

    def test_extract_answer_with_marker(self) -> None:
        cot = ChainOfThoughtPattern()
        response = "First, 2+2=4. Therefore, the answer is 4."
        assert "4" in cot.extract_answer(response)


class TestFewShot:
    def test_build_prompt(self) -> None:
        fs = FewShotPattern()
        examples = [{"input": "hello", "output": "greeting"}, {"input": "bye", "output": "farewell"}]
        result = fs.build_prompt("Classify intent", examples, "thanks")
        assert "Example 1" in result
        assert "thanks" in result

    def test_select_examples(self) -> None:
        fs = FewShotPattern()
        examples = [{"input": "python code error", "output": "debug"}, {"input": "billing question", "output": "billing"}]
        selected = fs.select_examples("I have a python error", examples, top_k=1)
        assert selected[0]["output"] == "debug"


class TestSelfConsistency:
    def test_majority_vote_unanimous(self) -> None:
        sc = SelfConsistencyPattern()
        result = sc.majority_vote(["Paris", "Paris", "Paris"])
        assert result["answer"] == "Paris"
        assert result["confidence"] == 1.0

    def test_majority_vote_split(self) -> None:
        sc = SelfConsistencyPattern()
        result = sc.majority_vote(["Paris", "Paris", "London"])
        assert result["answer"] == "Paris"
        assert result["confidence"] > 0.5


class TestRegression:
    def test_passes_valid_output(self) -> None:
        tester = PromptRegressionTester()
        tc = TestCase(test_id="t1", input_vars={}, expected_contains=["python"])
        result = tester.run_test(tc, "Python is a great language.")
        assert result.passed is True

    def test_fails_missing_content(self) -> None:
        tester = PromptRegressionTester()
        tc = TestCase(test_id="t2", input_vars={}, expected_contains=["java"])
        result = tester.run_test(tc, "Python is a great language.")
        assert result.passed is False


class TestABTester:
    def test_clear_winner(self) -> None:
        ab = ABTester()
        result = ab.compare([0.9, 0.85, 0.92], [0.6, 0.55, 0.58], "good", "bad")
        assert result.winner == "good"

    def test_equal_scores(self) -> None:
        ab = ABTester()
        result = ab.compare([0.8, 0.8], [0.8, 0.8])
        assert result.a_score == result.b_score

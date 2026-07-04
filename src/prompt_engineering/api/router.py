"""FastAPI router for prompt engineering endpoints."""
from fastapi import APIRouter
from prompt_engineering.patterns import ChainOfThoughtPattern, FewShotPattern, SelfConsistencyPattern
from prompt_engineering.testing import PromptRegressionTester, ABTester
from prompt_engineering.models.schemas import ABTestResult, TestCase
from prompt_engineering.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/prompts", tags=["prompt-engineering"])

_cot = ChainOfThoughtPattern()
_few_shot = FewShotPattern()
_self_consistency = SelfConsistencyPattern()
_regression = PromptRegressionTester()
_ab_tester = ABTester()


@router.post("/patterns/cot")
async def apply_cot(prompt: str, zero_shot: bool = True) -> dict:
    """Apply Chain-of-Thought pattern."""
    return {"modified_prompt": _cot.apply(prompt, zero_shot)}


@router.post("/patterns/few-shot")
async def build_few_shot(task: str, examples: list[dict], query: str) -> dict:
    """Build a few-shot prompt."""
    return {"prompt": _few_shot.build_prompt(task, examples, query)}


@router.post("/patterns/self-consistency/vote")
async def majority_vote(answers: list[str]) -> dict:
    """Run majority vote on multiple answers."""
    return _self_consistency.majority_vote(answers)


@router.post("/testing/ab-test", response_model=ABTestResult)
async def run_ab_test(scores_a: list[float], scores_b: list[float], name_a: str = "A", name_b: str = "B") -> ABTestResult:
    """Compare two prompt variants."""
    return _ab_tester.compare(scores_a, scores_b, name_a, name_b)


@router.get("/health")
async def health() -> dict:
    return {"status": "healthy", "service": "prompt-engineering-patterns"}

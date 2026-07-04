"""Pydantic schemas for prompt engineering."""
from datetime import datetime
from pydantic import BaseModel, Field


class PromptTemplate(BaseModel):
    """A versioned prompt template."""
    name: str = Field(description="Template name")
    version: int = Field(default=1)
    template: str = Field(description="Jinja2 template string")
    system_message: str = Field(default="")
    variables: list[str] = Field(default_factory=list)
    pattern: str = Field(default="direct", description="Pattern: direct, cot, few_shot, self_consistency, tree_of_thought")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TestCase(BaseModel):
    """A test case for prompt regression testing."""
    test_id: str = Field(description="Test case ID")
    input_vars: dict = Field(description="Template variable values")
    expected_contains: list[str] = Field(default_factory=list, description="Expected substrings in output")
    expected_not_contains: list[str] = Field(default_factory=list, description="Substrings that should NOT appear")
    min_quality_score: float = Field(default=0.7)


class TestResult(BaseModel):
    """Result of a single test case execution."""
    test_id: str
    passed: bool
    output: str = Field(default="")
    score: float = Field(default=0.0)
    reason: str = Field(default="")


class ABTestResult(BaseModel):
    """Result of an A/B test between two prompts."""
    prompt_a: str = Field(description="Prompt A name")
    prompt_b: str = Field(description="Prompt B name")
    winner: str = Field(description="Which prompt won")
    a_score: float = Field(default=0.0)
    b_score: float = Field(default=0.0)
    num_samples: int = Field(default=0)
    confidence: float = Field(default=0.0)
    significant: bool = Field(default=False)

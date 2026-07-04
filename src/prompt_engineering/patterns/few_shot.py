"""
Few-shot prompting pattern.

Provides examples of input-output pairs to guide LLM behavior
without fine-tuning.
"""

from prompt_engineering.config.settings import get_settings
from prompt_engineering.utils.logger import get_logger

logger = get_logger(__name__)


class FewShotPattern:
    """Constructs few-shot prompts from example pairs."""

    def __init__(self) -> None:
        self._settings = get_settings()

    def build_prompt(self, task_description: str, examples: list[dict[str, str]], query: str) -> str:
        """
        Build a few-shot prompt with examples.

        Args:
            task_description: Description of the task.
            examples: List of {"input": ..., "output": ...} dicts.
            query: The actual input to process.

        Returns:
            Formatted few-shot prompt.
        """
        max_examples = self._settings.patterns.few_shot_max_examples
        selected = examples[:max_examples]

        parts = [f"Task: {task_description}\n"]
        for i, example in enumerate(selected, 1):
            parts.append(f"Example {i}:")
            parts.append(f"Input: {example['input']}")
            parts.append(f"Output: {example['output']}\n")

        parts.append(f"Now process this:")
        parts.append(f"Input: {query}")
        parts.append(f"Output:")

        return "\n".join(parts)

    def select_examples(self, query: str, examples: list[dict[str, str]], top_k: int = 3) -> list[dict[str, str]]:
        """
        Select most relevant examples based on keyword overlap.

        Args:
            query: The input query.
            examples: All available examples.
            top_k: Number of examples to select.

        Returns:
            Most relevant examples.
        """
        query_terms = set(query.lower().split())
        scored = []
        for example in examples:
            example_terms = set(example["input"].lower().split())
            overlap = len(query_terms & example_terms)
            scored.append((overlap, example))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [ex for _, ex in scored[:top_k]]

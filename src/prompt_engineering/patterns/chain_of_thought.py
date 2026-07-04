"""
Chain-of-Thought (CoT) prompting pattern.

Instructs the LLM to reason step-by-step before providing a final answer,
improving accuracy on complex reasoning tasks.
"""

from prompt_engineering.utils.logger import get_logger

logger = get_logger(__name__)

COT_SUFFIX = "\n\nLet's think through this step by step:\n"
COT_ZERO_SHOT = "Think step by step before answering."


class ChainOfThoughtPattern:
    """Applies Chain-of-Thought reasoning to prompts."""

    def apply(self, prompt: str, zero_shot: bool = True) -> str:
        """
        Apply CoT pattern to a prompt.

        Args:
            prompt: Original prompt.
            zero_shot: If True, use zero-shot CoT. If False, append step-by-step suffix.

        Returns:
            Modified prompt with CoT instruction.
        """
        if zero_shot:
            return f"{prompt}\n\n{COT_ZERO_SHOT}"
        return f"{prompt}{COT_SUFFIX}"

    def extract_answer(self, response: str) -> str:
        """
        Extract the final answer from a CoT response.

        Looks for markers like 'Therefore', 'Final answer:', 'The answer is'.

        Args:
            response: Full CoT response with reasoning.

        Returns:
            Extracted final answer.
        """
        markers = ["therefore,", "final answer:", "the answer is", "in conclusion,"]
        response_lower = response.lower()

        for marker in markers:
            if marker in response_lower:
                idx = response_lower.rfind(marker)
                return response[idx + len(marker):].strip().split("\n")[0]

        # If no marker found, return last sentence
        sentences = [s.strip() for s in response.split(".") if s.strip()]
        return sentences[-1] + "." if sentences else response

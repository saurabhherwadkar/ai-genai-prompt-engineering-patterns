# AI GenAI Prompt Engineering Patterns

Production prompt engineering framework with CoT, few-shot, self-consistency patterns, A/B testing, regression testing, and prompt versioning.

## Key Learning Objectives

- Understand and implement Chain-of-Thought (CoT) prompting to guide LLMs through step-by-step reasoning for complex tasks
- Design effective few-shot prompts by selecting and structuring input-output examples for classification and formatting tasks
- Apply self-consistency sampling with majority voting to improve answer reliability and confidence
- Build reusable prompt templates using Jinja2 for consistent, maintainable prompt generation across projects
- Implement structured output prompting techniques to extract well-typed, schema-validated responses from LLMs
- Design system prompts that establish clear behavioral constraints, personas, and output formatting rules
- Conduct statistically rigorous A/B testing to compare prompt variants and select optimal strategies
- Build regression testing frameworks that detect prompt quality degradation across model updates and prompt changes
- Architect production-grade prompt engineering APIs with versioning, observability, and deployment best practices
- Apply prompt compression and optimization techniques to reduce token usage while preserving output quality

## Table of Contents
1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Patterns](#patterns)
4. [Deployment](#deployment)
5. [API Reference](#api-reference)
6. [Testing](#testing)

---

## End-to-End Flow

```mermaid
graph TD
    A[Raw Prompt] --> B{Pattern Selection}
    B -->|CoT| C[Add Step-by-Step Instruction]
    B -->|Few-Shot| D[Add Relevant Examples]
    B -->|Self-Consistency| E[Sample N Times → Vote]
    
    C & D & E --> F[Enhanced Prompt]
    F --> G[LLM Execution]
    G --> H[Output]
    
    H --> I[Regression Testing]
    I --> J{All Tests Pass?}
    J -->|No| K[Alert: Regression Detected]
    J -->|Yes| L[Safe to Deploy]
    
    H --> M[A/B Testing]
    M --> N[Compare Variants]
    N --> O[Statistical Significance Check]
    O --> P[Winner Selected]
```

---

## Patterns

| Pattern | Description | Best For |
|---------|-------------|----------|
| Chain-of-Thought | Step-by-step reasoning | Math, logic, complex reasoning |
| Few-Shot | Input-output examples | Classification, formatting |
| Self-Consistency | Multiple samples + majority vote | High-confidence answers |

---

## Project Structure

```
ai-genai-prompt-engineering-patterns/
├── src/prompt_engineering/
│   ├── patterns/
│   │   ├── chain_of_thought.py  # CoT zero-shot and manual
│   │   ├── few_shot.py          # Example-based prompting
│   │   └── self_consistency.py  # Majority voting
│   ├── testing/
│   │   ├── regression.py        # Prompt regression tests
│   │   └── ab_test.py           # A/B statistical comparison
│   ├── api/router.py
│   └── main.py
├── tests/
├── config/
├── pyproject.toml, Dockerfile, docker-compose.yml
```

---

## Deployment

```bash
poetry install && cp .env.example .env
poetry run python -m uvicorn prompt_engineering.main:app --reload --port 8000
poetry run pytest
docker-compose up --build
```

---

## API Reference

| Endpoint | Description |
|----------|-------------|
| POST /api/v1/prompts/patterns/cot | Apply Chain-of-Thought |
| POST /api/v1/prompts/patterns/few-shot | Build few-shot prompt |
| POST /api/v1/prompts/patterns/self-consistency/vote | Majority vote |
| POST /api/v1/prompts/testing/ab-test | A/B test comparison |

---

## Testing

```bash
poetry run pytest --cov=src/prompt_engineering --cov-report=term-missing
```

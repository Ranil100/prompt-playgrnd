def build_prompt(strategy: str, task: str) -> str:
    if strategy == "zero-shot":
        return f"""Complete the user's task directly and clearly.

USER TASK:
{task}
"""

    if strategy == "few-shot":
        return f"""Complete the user's task using the examples below as guidance.

EXAMPLE 1
Task: Summarize: "The project meeting is moved from Tuesday to Thursday at 3 PM. Please review the design document beforehand."
Answer: "The project meeting moved to Thursday at 3 PM. Review the design document beforehand."

EXAMPLE 2
Task: Extract action items: "Please send the invoice today and confirm tomorrow's delivery."
Answer:
1. Send the invoice today.
2. Confirm tomorrow's delivery.

Now complete this task:
{task}
"""

    if strategy == "structured":
        return f"""Complete the task below using a concise, structured approach.

Requirements:
- Identify the user's actual objective.
- Extract the important facts or constraints.
- Avoid irrelevant information.
- Produce a clear final answer.
- Do not reveal private chain-of-thought or hidden reasoning.
- Prefer headings, bullets, or numbered steps when they improve clarity.

TASK:
{task}
"""

    raise ValueError(f"Unknown strategy: {strategy}")

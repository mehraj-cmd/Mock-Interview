# Interview Answer Grading Rubric

This rubric defines what separates a strong answer from a weak one, for two question types: **Technical** and **Behavioral**. Each dimension is scored 1–5, with descriptors for what a low, mid, and high score looks like.

---

## A. Technical Questions

Evaluate every technical answer on three dimensions: **Correctness**, **Clarity of Explanation**, and **Structure**.

### 1. Correctness (Is the answer actually right?)

| Score | Description |
|---|---|
| 1–2 (Weak) | Answer is factually wrong, or the proposed solution doesn't solve the actual problem asked. Misses key edge cases entirely. |
| 3 (Average) | Core answer is correct but has minor errors, or misses 1–2 edge cases (e.g., empty input, duplicates, negative numbers). |
| 4–5 (Strong) | Answer is fully correct, handles edge cases proactively, and — where relevant — discusses time/space complexity or trade-offs without being asked. |

**Weak example:** Candidate says an unsorted array can be searched in O(log n) using binary search.
**Strong example:** Candidate correctly identifies binary search requires a sorted array, states the correct O(log n) complexity, and mentions what happens with duplicate values.

### 2. Clarity of Explanation (Can they teach it, not just do it?)

| Score | Description |
|---|---|
| 1–2 (Weak) | Rambling, jumps between ideas, uses jargon without defining it, or the interviewer has to ask multiple follow-ups just to understand what the candidate means. |
| 3 (Average) | Understandable but requires some effort to follow; explanation is correct but not concise. |
| 4–5 (Strong) | Explains the "why" behind the approach before diving into "how." Uses simple language, defines terms, and checks for understanding (e.g., "does that make sense so far?"). |

### 3. Structure (Did they follow a logical process?)

| Score | Description |
|---|---|
| 1–2 (Weak) | Jumps straight to code/answer with no plan. No discussion of approach, no mention of alternatives. |
| 3 (Average) | States an approach before answering, but doesn't compare it to alternatives or discuss trade-offs. |
| 4–5 (Strong) | Follows a clear process: clarify the question → state assumptions → propose approach → discuss alternatives/trade-offs → implement/answer → test with an example. |

**Overall Technical Score** = average of the three dimensions above (or weight Correctness higher, e.g., 50/25/25, if your project wants a single weighted score).

---

## B. Behavioral Questions (STAR Method)

Behavioral answers are graded on how completely and specifically they cover each STAR component.

| Component | What it should contain | Weak signal | Strong signal |
|---|---|---|---|
| **S — Situation** | Specific context: when, where, what was the setting | Vague ("at my last job, something happened") | Specific and time-bound ("During my final year project in Feb 2025, our team of 4 was building...") |
| **T — Task** | The candidate's specific responsibility or goal in that situation | Confuses "task" with "action" — no clear personal responsibility stated | Clearly states what they personally were responsible for, distinct from the team's goal |
| **A — Action** | What the candidate specifically did — not what "the team" did | Uses "we" throughout, no individual contribution is clear; lists actions with no reasoning | Uses "I" for their own contribution, explains their reasoning/decision-making, shows initiative |
| **R — Result** | A measurable or clearly observable outcome, plus a reflection/learning | No outcome stated, or outcome is vague ("it worked out well") | Quantified or concrete outcome ("reduced load time by 30%", "shipped 2 weeks early") + what they learned or would do differently |

### Scoring Guide

| Score | Description |
|---|---|
| 1–2 (Weak) | Missing 2+ STAR components entirely, or answer is generic/could apply to any situation. |
| 3 (Average) | All 4 components present but shallow — e.g., result is unquantified, or action doesn't show clear individual ownership. |
| 4–5 (Strong) | All 4 components present, specific, individually-owned action, and a measurable/clear result with genuine reflection. |

### Red Flags (auto-downgrade regardless of STAR structure)
- Blaming others entirely for a failure with no self-reflection
- Answer contradicts something said earlier in the interview
- Overly rehearsed/generic answer that doesn't reference specific details when probed

---

## Suggested Overall Scoring Bands (for combining into a final verdict)

| Total Avg Score | Verdict |
|---|---|
| 4.0 – 5.0 | Strong Hire |
| 3.0 – 3.9 | Hire (with reservations) |
| 2.0 – 2.9 | Weak — needs more evidence |
| Below 2.0 | No Hire |

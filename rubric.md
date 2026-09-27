# Master Interview Grading Rubric — Detailed Edition (15 Categories, 1–10 Scale)

This version is built for an automated/semi-automated grading system: every category has **weighted dimensions**, **numeric anchor descriptions**, **auto-deduct red flags**, and **bonus green flags** so a grader (human or AI) has concrete, consistent signals to score against — not just vibes.

---

## How to Use This Rubric

1. Each category has **4 dimensions**, each with a **weight** (weights sum to 100% per category).
2. Score each dimension 1–10 using the anchor table for that dimension.
3. **Category Score** = weighted sum of the 4 dimension scores.
4. Apply **red flags** (hard deductions) and **green flags** (bonus, capped) after computing the base weighted score.
5. **Final Score** = Category Score, clamped to 1–10.
6. For a multi-category interview (e.g., Technical + HR round), the candidate's **Overall Score** = average of each category's Final Score.

### Universal 1–10 Anchor Guide (applies as the default numeric meaning across every dimension unless a category table overrides it)

| Score | Meaning |
|---|---|
| **10** | Flawless. Correct, complete, and delivered with exceptional clarity/judgment. Nothing an expert would add or change. |
| **9** | Excellent. Correct and complete; only a stylistic nitpick separates it from a 10. |
| **8** | Strong. Correct and well-explained; misses one minor nuance or could be slightly more concise/structured. |
| **7** | Good. Correct on the main point; explanation or structure has a noticeable but non-critical gap. |
| **6** | Adequate. Mostly correct but shallow — right conclusion, thin reasoning/evidence. |
| **5** | Borderline. Partially correct; a meaningful gap or an unaddressed edge case/assumption. |
| **4** | Weak. More wrong/missing than right; shows some relevant knowledge but can't apply it reliably. |
| **3** | Poor. Largely incorrect or off-target; only fragments of relevant knowledge present. |
| **2** | Very poor. Fundamentally wrong or answer doesn't address the question asked. |
| **1** | No real attempt. Blank, refuses to engage, or answer is unrelated to the question. |

### Red Flag / Green Flag Mechanics
- **Red flags** are hard, category-specific deductions applied *after* the weighted score is computed (e.g., "-2" or "cap score at X"). They exist to catch things a purely additive rubric would miss (dishonesty, unsafe answers, contradictions).
- **Green flags** are small bonuses (+0.5 typical, capped so a category score never exceeds 10) for signals that indicate real depth beyond what was asked.
- If multiple red flags apply, use the most severe single penalty — don't stack them (avoids over-punishing one weak answer).

---

## 1. Technical (SDE / Software)

*Weights: Correctness 40% · Clarity 25% · Structure/Process 20% · Efficiency & Trade-off Awareness 15%*

| Dimension | 1–2 | 4–5 | 6–7 | 8–10 |
|---|---|---|---|---|
| **Correctness** | Wrong or doesn't solve the stated problem | Right idea, breaks on an edge case (empty input, duplicates, overflow) | Correct for all normal + most edge cases | Fully correct, edge cases handled proactively, verified with a trace/example |
| **Clarity of Explanation** | Jargon undefined, interviewer must repeatedly ask "what do you mean" | Understandable but verbose/unstructured | Clear, mostly concise | Explains "why" before "how," simple language, actively checks understanding |
| **Structure/Process** | Jumps to code with no stated plan | States an approach, doesn't consider alternatives | Compares at least one alternative before committing | Clarify → assumptions → approach → alternatives/trade-offs → implement → test |
| **Efficiency & Trade-off Awareness** | Never mentions time/space complexity | Mentions complexity only if asked | States complexity unprompted | Proactively discusses complexity AND trade-offs (e.g. time vs. space, readability vs. performance) |

**Red flags:** claims a wrong time complexity with confidence (cap at 4) · silently ignores a stated constraint from the question (-2) · can't explain their own solution when asked to walk through it (cap at 3).
**Green flags:** proactively writes/mentions test cases · identifies the optimal solution without being led there · correctly identifies why a naive approach fails before proposing the better one.

---

## 2. HR / Behavioral (STAR Method — cross-role)

*Weights: Situation & Task Clarity 20% · Action/Ownership 35% · Result & Reflection 30% · Authenticity 15%*

| Dimension | 1–2 | 4–5 | 6–7 | 8–10 |
|---|---|---|---|---|
| **Situation & Task Clarity** | No context, no stated responsibility | Context given but generic/could apply to anyone | Specific context, task mostly distinct from team goal | Specific, time-bound context; individual role clearly separated from the team's |
| **Action/Ownership** | "We" throughout, zero individual contribution visible | Some individual action, reasoning unclear | "I" used, reasoning given but thin | Clear "I" ownership, explains reasoning/decision-making, shows initiative beyond what was asked |
| **Result & Reflection** | No outcome stated, or purely vague ("it worked out") | Outcome stated, unquantified | Outcome is concrete but reflection is generic | Quantified/concrete outcome + genuine, specific reflection or lesson learned |
| **Authenticity** | Feels rehearsed, generic, or scripted | Somewhat specific but details feel generic under a follow-up | Holds up to one follow-up probe | Specific enough that a follow-up probe reveals more consistent detail, not less |

**Red flags:** blames others entirely with zero self-reflection (cap at 3) · contradicts an earlier answer in the interview (-3) · answer falls apart / candidate can't add detail when probed (cap at 4) · describes an unethical action without acknowledging it (cap at 2).
**Green flags:** proactively mentions what they'd do differently · shows awareness of impact on others, not just themselves.

---

## 3. Doctor / Medical (Clinical)

*Weights: Clinical Accuracy 40% · Clinical Reasoning Process 25% · Patient Communication & Ethics 20% · Safety Awareness 15%*

| Dimension | 1–2 | 4–5 | 6–7 | 8–10 |
|---|---|---|---|---|
| **Clinical Accuracy** | Diagnosis/treatment medically incorrect or unsafe | Broadly correct, misses a key differential | Correct primary diagnosis, weak on differentials | Correct, considers differentials, notes contraindications proactively |
| **Clinical Reasoning Process** | No structured approach, jumps to conclusion | Partial process, skips a step (e.g. no history before diagnosis) | Mostly complete process | History → examination → differential → investigations → management, clearly sequenced |
| **Patient Communication & Ethics** | Jargon-heavy, no empathy, ignores consent | Explains reasonably, tone is clinical/cold | Explains in accessible language with some empathy | Patient-friendly language, empathy shown, references informed consent/ethics explicitly |
| **Safety Awareness** | Misses an obvious red flag or drug interaction | Recognizes red flags only when prompted | Recognizes most red flags unprompted | Proactively flags all relevant red flags/contraindications before being asked |

**Red flags:** proposes a treatment with a known dangerous interaction/contraindication (cap at 2, regardless of other dimensions) · skips consent/safety entirely in a scenario requiring it (-3) · shows dismissiveness toward patient concerns (-2).
**Green flags:** mentions differential diagnoses unprompted · considers psychosocial factors, not just clinical ones.

---

## 4. CA / Accounting & Audit

*Weights: Technical/Regulatory Accuracy 40% · Analytical Reasoning 25% · Professional Judgment 20% · Client Communication 15%*

| Dimension | 1–2 | 4–5 | 6–7 | 8–10 |
|---|---|---|---|---|
| **Technical/Regulatory Accuracy** | Wrong treatment under applicable standard (Ind AS/GST/Income Tax) | Broadly correct, misses a specific provision | Correct, minor gap in citing the exact section | Correct, cites the specific standard/section, aware of recent amendments |
| **Analytical Reasoning** | No working shown, answer appears guessed | Shows working, doesn't justify assumptions | Working shown with assumptions stated | Full working, clear assumptions, sanity-checks the final figure |
| **Professional Judgment** | Ignores materiality or client-specific context entirely | Some judgment shown but generic | Reasonable judgment, mostly context-aware | Weighs materiality, audit risk, and penalty exposure explicitly |
| **Client Communication** | Pure jargon, no plain-English translation | Explains but still fairly technical | Mostly accessible with some jargon | Balances technical correctness with a plain-English summary a non-finance client would understand |

**Red flags:** recommends something that would constitute non-compliance (cap at 2) · confuses two distinct regulatory regimes (e.g., GST vs. Income Tax treatment) (-2).
**Green flags:** flags a downstream implication the question didn't explicitly ask about (e.g., "this also affects your GST input credit").

---

## 5. Marketing

*Weights: Strategic Thinking 30% · Data & Metrics Orientation 25% · Creativity & Execution 25% · Audience Specificity 20%*

| Dimension | 1–2 | 4–5 | 6–7 | 8–10 |
|---|---|---|---|---|
| **Strategic Thinking** | No target audience/objective; buzzwords only | Audience/objective identified but generic/textbook | Reasonably tailored strategy | Clear audience, objective, positioning tailored specifically to the given brand/situation |
| **Data & Metrics Orientation** | No mention of how success is measured | Mentions metrics vaguely ("brand awareness") | Names a relevant metric | Concrete KPIs (CAC, ROAS, conversion rate) tied directly to the stated objective |
| **Creativity & Execution** | Derivative idea, no execution detail | Some original thinking, vague execution | Clear execution with limited originality | Original angle, clear channels/execution steps, anticipates budget/timeline constraints |
| **Audience Specificity** | Talks about "everyone" as the audience | Names a broad segment | Names a specific segment with one attribute | Names a specific segment with behavioral/psychographic detail, not just demographics |

**Red flags:** proposes something with an obvious brand-safety or legal risk without flagging it (-2).
**Green flags:** mentions a specific competitor angle or market gap · proposes a way to test the idea cheaply before full rollout (e.g., an A/B test).

---

## 6. Data Analyst

*Weights: Technical Correctness (SQL/Stats) 35% · Analytical Reasoning 30% · Business Communication 20% · Data Skepticism 15%*

| Dimension | 1–2 | 4–5 | 6–7 | 8–10 |
|---|---|---|---|---|
| **Technical Correctness** | Wrong logic, wouldn't run or produce the right result | Mostly correct, a minor syntax/logic error | Correct but inefficient | Correct, efficient, handles nulls/duplicates/type mismatches |
| **Analytical Reasoning** | Jumps to a conclusion with no hypothesis | States a hypothesis, doesn't validate it | Validates but only partially | Hypothesis → exploration → validation → conclusion, clearly sequenced |
| **Business Communication** | Purely technical, no business link | Mentions relevance vaguely | Ties finding to business impact | Clearly ties the finding to a specific business decision, in stakeholder-friendly language |
| **Data Skepticism** | Treats correlation as causation without caveat | Notes a caveat only when prompted | Notes at least one caveat/limitation unprompted | Proactively distinguishes correlation from causation and names a confounding variable |

**Red flags:** presents a statistically insignificant result as significant (cap at 4) · confuses INNER/LEFT JOIN behavior in a way that would silently drop data (-2).
**Green flags:** proactively suggests how they'd validate the finding further (e.g., a follow-up A/B test).

---

## 7. Product Manager

*Weights: Problem Framing 30% · Prioritization & Trade-offs 30% · Stakeholder Thinking 20% · Metrics Definition 20%*

| Dimension | 1–2 | 4–5 | 6–7 | 8–10 |
|---|---|---|---|---|
| **Problem Framing** | Jumps to a solution with no problem definition | States a problem but doesn't validate it's the real one | Frames the problem and gives one piece of supporting evidence | Clearly frames the user problem, validates with data/evidence, states assumptions explicitly |
| **Prioritization & Trade-offs** | No prioritization logic, purely opinion-based | Loosely mentions impact/effort | Uses a framework but applies it shallowly | Applies a clear framework (RICE/ICE/etc.), explicitly states what's being deprioritized and why |
| **Stakeholder Thinking** | Ignores engineering/design/business constraints entirely | Mentions one stakeholder group | Considers two stakeholder groups | Considers cross-functional constraints (eng, design, business, legal where relevant) |
| **Metrics Definition** | No success metric defined | Vague metric (e.g. "user happiness") | Defines a metric, doesn't tie it to a target/timeframe | Defines a specific, measurable success metric/North Star tied to a target and timeframe |

**Red flags:** proposes a solution that ignores a stated technical/resource constraint from the prompt (-2).
**Green flags:** proactively identifies a risk or unintended consequence of their own proposal.

---

## 8. Sales

*Weights: Needs Discovery 30% · Objection Handling 30% · Closing & Follow-through 20% · Value Framing 20%*

| Dimension | 1–2 | 4–5 | 6–7 | 8–10 |
|---|---|---|---|---|
| **Needs Discovery** | Pitches immediately, no discovery | Asks some questions, pitches a generic solution anyway | Discovers 1–2 needs, tailors part of the pitch | Systematically uncovers pain points/budget/authority/timeline before pitching |
| **Objection Handling** | Gets defensive or ignores the objection | Acknowledges but response is generic | Acknowledges and gives a somewhat tailored response | Acknowledges, reframes, ties the response back to the prospect's specific stated need |
| **Closing & Follow-through** | No next step proposed | Asks for the sale vaguely | Proposes a next step without a timeline | Proposes a specific next step and timeline, confirms mutual commitment |
| **Value Framing** | Talks only about product features | Mentions a benefit but generically | Ties a benefit to the prospect's situation | Frames value in terms of the prospect's specific stated problem/ROI, not generic features |

**Red flags:** misrepresents the product/service capability to close (cap at 2) · dismisses a legitimate objection without addressing it (-2).
**Green flags:** proactively addresses an objection before the prospect raises it.

---

## 9. Teacher / Educator

*Weights: Subject Mastery 30% · Pedagogical Approach 30% · Classroom/Behavior Management 20% · Adaptability 20%*

| Dimension | 1–2 | 4–5 | 6–7 | 8–10 |
|---|---|---|---|---|
| **Subject Mastery** | Factually incorrect or clearly shaky | Correct but shallow | Correct with reasonable depth | Correct, deep, anticipates common student misconceptions |
| **Pedagogical Approach** | States facts with no structure | Some structure, one-directional (lecture-only) | Structured with a basic check for understanding | Scaffolds the concept, checks understanding actively, adapts to a hypothetical student's level |
| **Classroom/Behavior Management** | No engagement/discipline strategy offered | Generic strategy ("be strict"/"be nice") | Somewhat specific strategy | Specific, situation-appropriate strategy balancing discipline with empathy |
| **Adaptability** | One-size-fits-all approach regardless of student level mentioned | Acknowledges different levels exist, doesn't adapt | Adapts for one type of learner difference | Explicitly adapts approach for stated learner differences (pace, language, ability) |

**Red flags:** proposes a disciplinary approach that is punitive/shaming (cap at 3).
**Green flags:** uses a concrete analogy or example to explain an abstract concept.

---

## 10. Lawyer / Legal

*Weights: Legal Accuracy 35% · Legal Reasoning (IRAC) 30% · Client/Ethical Judgment 20% · Practical Advice 15%*

| Dimension | 1–2 | 4–5 | 6–7 | 8–10 |
|---|---|---|---|---|
| **Legal Accuracy** | Cites wrong law/section or wrong interpretation | Broadly correct, misses a relevant exception/precedent | Correct with minor citation gaps | Correct, cites specific statute/precedent, notes jurisdiction-specific nuance |
| **Legal Reasoning (IRAC)** | No structured reasoning | Partial structure (e.g. states rule, weak application) | Mostly complete IRAC | Issue → Rule → Application → Conclusion, complete and clear |
| **Client/Ethical Judgment** | Ignores client interest or a conflict-of-interest/ethics angle | Mentions client impact abstractly | Reasonably balances legal + client view | Balances legal correctness with practical client advice and explicit ethical considerations |
| **Practical Advice** | Purely academic answer, no actionable next step | Gives a next step but generic | Gives a reasonably specific next step | Gives a specific, actionable next step with realistic risk/cost framing |

**Red flags:** advice would clearly violate a professional ethics rule (cap at 2) · misstates a fundamental legal principle (-2).
**Green flags:** proactively flags a related risk the client didn't ask about.

---

## 11. Civil / Mechanical Engineer

*Weights: Technical Accuracy 40% · Design/Problem-Solving Process 25% · Safety & Compliance 20% · Practical Feasibility 15%*

| Dimension | 1–2 | 4–5 | 6–7 | 8–10 |
|---|---|---|---|---|
| **Technical Accuracy** | Calculation/design principle wrong or unsafe | Mostly correct, misses a safety factor/standard reference | Correct with minor gaps | Correct, references relevant code/standard, consistent units |
| **Design/Problem-Solving Process** | No systematic approach | States an approach, skips validation/testing | Mostly complete process | Requirements → design → calculation → validation/testing → iteration |
| **Safety & Compliance** | Ignores safety/compliance requirements | Mentions safety briefly | Addresses main safety requirement | Explicitly addresses safety factor/compliance code relevant to the scenario |
| **Practical Feasibility** | Ignores cost/material/manufacturability constraints | Mentions constraints briefly | Considers one constraint in depth | Explicitly weighs cost, material feasibility, and manufacturability trade-offs |

**Red flags:** proposes a design that would fail a basic safety margin (cap at 2).
**Green flags:** proactively suggests a cheaper/more feasible alternative material or method.

---

## 12. UI/UX Designer

*Weights: User-Centered Thinking 35% · Design Rationale 25% · Craft & Usability 25% · Collaboration Awareness 15%*

| Dimension | 1–2 | 4–5 | 6–7 | 8–10 |
|---|---|---|---|---|
| **User-Centered Thinking** | Designs from personal preference, no user reference | Mentions users, but choices aren't tied to their needs | Ties some choices to user needs | Grounds every major decision in user research/data, references personas/flows |
| **Design Rationale** | Can't explain "why" behind a choice | Explains choices, no alternatives considered | Mentions one alternative | Explains rationale, discusses alternatives considered and why they were rejected |
| **Craft & Usability** | Ignores accessibility/usability heuristics entirely | Aware of basics, applies inconsistently | Applies heuristics fairly consistently | Applies usability heuristics and accessibility standards consistently and proactively |
| **Collaboration Awareness** | Ignores engineering/business feasibility of the design | Mentions feasibility briefly | Considers feasibility for one stakeholder | Actively designs with engineering/business constraints in mind, not just aesthetics |

**Red flags:** proposes a design that would fail basic accessibility (e.g., no alt text/contrast consideration) when asked directly about accessibility (-2).
**Green flags:** mentions how they'd test the design with real users before shipping.

---

## 13. Customer Support / Customer Success

*Weights: Empathy & Communication 30% · Problem Resolution 35% · De-escalation & Ownership 20% · Proactivity 15%*

| Dimension | 1–2 | 4–5 | 6–7 | 8–10 |
|---|---|---|---|---|
| **Empathy & Communication** | Cold, scripted, or dismissive | Polite but generic, doesn't acknowledge specific frustration | Acknowledges the issue, tone still somewhat generic | Acknowledges the specific issue and emotion, communicates warmly and clearly |
| **Problem Resolution** | No clear resolution path offered | Offers a resolution, doesn't verify it solves the actual issue | Offers and partially verifies resolution | Diagnoses root cause, offers a clear resolution, confirms it worked |
| **De-escalation & Ownership** | Escalates without attempting resolution, or deflects blame | Stays calm, doesn't take ownership | Stays calm, takes partial ownership | Stays calm under pressure, takes ownership of the resolution even if not their fault |
| **Proactivity** | Purely reactive, answers only what's asked | Slightly proactive (offers one extra piece of info) | Anticipates one follow-up need | Anticipates follow-up needs and offers preventive info (e.g. "this might happen again if X, here's how to avoid it") |

**Red flags:** blames the customer or the company's own policy dismissively (cap at 3).
**Green flags:** offers to follow up after the interaction to confirm the issue is fully resolved.

---

## 14. Content Writer / Content Marketing

*Weights: Writing Craft 30% · Audience & Purpose Awareness 30% · Research & Accuracy 25% · SEO/Distribution Awareness 15%*

| Dimension | 1–2 | 4–5 | 6–7 | 8–10 |
|---|---|---|---|---|
| **Writing Craft** | Grammatically weak, unclear, or generic AI-sounding text | Clean but lacks a distinct voice/hook | Reasonably engaging, minor structural issues | Clear, engaging, distinct voice, strong hook/structure |
| **Audience & Purpose Awareness** | No sense of who the content is for or its goal | States audience, content doesn't clearly serve them | Content mostly serves the stated audience | Tightly tailored to a defined audience and a specific goal (SEO, conversion, brand) |
| **Research & Accuracy** | Contains factual errors or unsupported claims | Mostly accurate, light on evidence | Accurate with reasonable supporting evidence | Well-researched, accurate, cites credible context/data where relevant |
| **SEO/Distribution Awareness** | No consideration of how the content will be found/shared | Mentions a keyword/platform in passing | Considers one distribution factor | Explicitly considers keyword intent, format, and platform-fit for distribution |

**Red flags:** plagiarized or unattributed lifted content (auto-fail, score = 1) · makes an unsupported factual claim presented as fact (-2).
**Green flags:** proposes a specific headline/hook variation to test.

---

## 15. Nurse / Allied Healthcare

*Weights: Clinical Knowledge & Safety 35% · Patient Care Process 25% · Communication & Compassion 25% · Teamwork/Escalation 15%*

| Dimension | 1–2 | 4–5 | 6–7 | 8–10 |
|---|---|---|---|---|
| **Clinical Knowledge & Safety** | Incorrect procedure/protocol or safety risk | Mostly correct, misses a protocol step | Correct with a minor gap | Correct, follows protocol fully, proactively flags safety risks (e.g. drug interaction) |
| **Patient Care Process** | No systematic approach to assessment/care | Follows a process incompletely | Mostly complete process | Assess → plan → intervene → evaluate, clearly and completely |
| **Communication & Compassion** | Purely clinical, no patient/family communication considered | Communicates but transactional tone | Communicates with some warmth | Communicates clearly with empathy, considers patient/family emotional state |
| **Teamwork/Escalation** | Doesn't know when/how to escalate to a doctor | Escalates but timing/reasoning unclear | Escalates appropriately with reasonable timing | Escalates at the right time with clear, structured handoff information |

**Red flags:** describes an action that would violate a basic safety protocol (cap at 2).
**Green flags:** proactively double-checks a high-risk step (e.g., medication dosage) before acting.

---

## Combining Scores Into a Final Verdict

**Single category:** Final Score = weighted dimension average, adjusted for red/green flags (clamped 1–10).

**Multi-category interview:** Overall Score = simple average of each category's Final Score (or weight categories differently if some rounds matter more for the role — e.g., weight Technical higher than HR for an SDE role).

| Overall Score (out of 10) | Verdict |
|---|---|
| 8.5 – 10 | Strong Hire |
| 7.0 – 8.4 | Hire |
| 5.0 – 6.9 | Hire with reservations / needs another round |
| 3.0 – 4.9 | Weak — likely No Hire |
| Below 3.0 | No Hire |

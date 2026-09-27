# Mock Interview — Master Reference Doc

This is the single combined reference for the AI model's context — the grading rubric, the interview question reference, and resume + question + answer examples all in one place. Paste the relevant section into Antigravity prompts wherever needed (Question Maker, Grading System), and use this as the one source of truth so nothing conflicting is scattered across the backend.

---

## PART 1 — GRADING RUBRIC

### Mock Interview Grading Rubric

This is the rubric your grading system (Step 6) will use. It's built the way real hiring teams build interview rubrics: instead of one vague "good/bad" judgment, each answer is scored on a few specific dimensions, each with clear descriptions of what a weak vs. strong answer looks like at each score level. This is what makes AI feedback feel specific instead of generic.

---

### Part A — Technical Question Rubric

Score each answer 1–5 on these four dimensions, then average them for the overall score.

#### 1. Relevance
*Did they actually answer the question asked, or drift off-topic?*

| Score | What it looks like |
|---|---|
| **1** | Answer doesn't address the actual question at all |
| **2** | Mostly off-topic, touches the question briefly |
| **3** | Addresses the question but misses part of what was asked |
| **4** | Directly addresses the question with minor gaps |
| **5** | Fully addresses every part of what was asked |

#### 2. Depth & Correctness
*Is the technical content actually correct and detailed enough?*

| Score | What it looks like |
|---|---|
| **1** | Factually wrong or no real technical content |
| **2** | Surface-level, mostly buzzwords with little substance |
| **3** | Correct but generic — doesn't go beyond the obvious |
| **4** | Correct and reasonably detailed, shows real understanding |
| **5** | Correct, detailed, and shows deeper reasoning (e.g., explains *why*, not just *what*) |

#### 3. Structure & Clarity
*Could someone follow the explanation without already knowing the answer?*

| Score | What it looks like |
|---|---|
| **1** | Rambling, no clear order, hard to follow |
| **2** | Some structure but jumps around |
| **3** | Understandable but not clearly organized |
| **4** | Clear step-by-step or logical structure |
| **5** | Clean, well-organized, easy to follow even for a non-expert |

#### 4. Trade-off Awareness
*Did they show awareness of alternatives, limitations, or trade-offs (not just one "right" answer)?*

| Score | What it looks like |
|---|---|
| **1** | No awareness of any alternatives or limitations |
| **2** | Briefly mentions an alternative without explanation |
| **3** | Mentions one trade-off with some reasoning |
| **4** | Discusses multiple trade-offs (e.g., speed vs. cost, simplicity vs. scale) |
| **5** | Weighs multiple trade-offs and justifies the choice made |

**Overall Technical Score** = average of the four scores above (rounded to nearest 0.5)

---

### Part B — Behavioral / HR Question Rubric (STAR-based)

Score each answer 1–5 on how well it covers the STAR structure, plus two extra checks that matter a lot in real evaluations: ownership and outcome.

#### 1. Situation — Did they set clear context?

| Score | What it looks like |
|---|---|
| **1** | No context given at all |
| **2** | Vague context ("at my last job...") |
| **3** | Some context but missing key details (when, what, why it mattered) |
| **4** | Clear context that sets up the story well |
| **5** | Concise, specific context that immediately makes the situation clear |

#### 2. Task — Did they explain what needed to be done?

| Score | What it looks like |
|---|---|
| **1** | No mention of what the actual task/goal was |
| **2** | Task is implied but not clearly stated |
| **3** | Task is stated but vague |
| **4** | Task is clearly and specifically stated |
| **5** | Task is clear, specific, and its importance/stakes are explained |

#### 3. Action — Did they explain what *they* personally did (not just "we")?

| Score | What it looks like |
|---|---|
| **1** | No specific actions mentioned |
| **2** | Vague actions, mostly describes what "the team" did |
| **3** | Some personal actions mentioned, mixed with team actions |
| **4** | Clear, specific actions the candidate personally took |
| **5** | Clear, specific personal actions with reasoning for why they chose that approach |

> **Important**: This is one of the biggest real-world evaluation signals — flag answers that say "we did X" repeatedly without ever saying "I did X." That's a common weak spot to call out in feedback.

#### 4. Result — Did they mention the outcome?

| Score | What it looks like |
|---|---|
| **1** | No outcome mentioned at all |
| **2** | Vague outcome ("it worked out fine") |
| **3** | Outcome mentioned but not clearly tied to their action |
| **4** | Clear outcome, connected to what they did |
| **5** | Clear outcome with specifics — a number, a measurable change, or a concrete result |

**Overall Behavioral Score** = average of the four STAR scores above (rounded to nearest 0.5)

---

### Part C — Rules for Writing Feedback (very important)

Give this to the AI as a strict instruction — this is what separates useful feedback from empty praise:
1. **Never write vague feedback** like "could be clearer" or "good effort." Always name the specific thing that was missing or strong.
   - *Bad*: "Your answer could be more detailed."
   - *Good*: "You didn't mention what happens if the API call fails — add a fallback/error-handling case."
2. **Always reference something the candidate actually said**, quoting or paraphrasing their own words, so the feedback feels tied to their real answer, not generic.
3. **For technical answers**, if trade-off awareness scored low, explicitly suggest what trade-off they missed.
4. **For behavioral answers**, if the Action score is low because of "we" language, explicitly point that out ("You described what the team did, but not your specific role — try naming exactly what you did").
5. **Keep feedback to 2–4 sentences per answer** — long enough to be useful, short enough to actually be read.

---

### Part D — Overall Report Card Scoring

Once all questions are graded:
* **Overall score** = average of all individual question scores (technical + behavioral combined)
* **Top improvement areas** = pick the 2–3 lowest-scoring dimensions across all answers (e.g., if Trade-off Awareness and Action/ownership were consistently weak, those become the report's main takeaways) — don't just list every weakness, prioritize the ones that repeated most.

---

## PART 2 — INTERVIEW QUESTION REFERENCE (What to Ask, By Role)

### Interview Questions Reference — What to Ask, By Role

This is reference material for Step 4 (Question Maker). Paste the relevant role's questions into your prompt as examples, so generated questions feel realistic instead of generic.

---

### Part A — What Makes a Good Interview Question

Before listing questions, here's what separates a good one from a weak one — this matters because your Question Maker should be generating questions with these same qualities.

A good question is:
1. **Specific enough to test real understanding, not just memory** — "What is a linked list?" is weak. "How would you optimize a slow-running SQL query?" is strong, because it forces reasoning, not just a definition.
2. **Tied to what the candidate actually claims** — if a resume mentions a specific project or tool, a good interviewer asks about that, not a generic version of it. Real interview reports show this pattern clearly: interviewers frequently ask candidates to explain their own listed projects from scratch, or rate their own familiarity with the technologies they listed.
3. **Layered with a natural follow-up** — real interviews often start broad then narrow (explain the approach, then its time/space complexity).
4. **Balanced across three types** — most real interview loops mix three categories rather than only one:
   - **Technical/knowledge questions** (concepts, definitions, how something works)
   - **Problem-solving questions** (applying knowledge to a new scenario)
   - **Behavioral questions** (past experience, teamwork, handling pressure)

Your Question Maker prompt should generate a mix of these three types, not all from one category.

---

### Part B — Sample Questions by Role

#### Software Developer / SDE (Technical)

Real SDE interviews commonly draw from a fixed set of technical topics: the difference between a class and an object in OOP, implementing a factorial function, the differences between SQL and NoSQL databases, and how to optimize a web application's performance. Interview reports also show frequent focus on OOP vs. procedural programming, SQL joins, garbage collection, REST vs. SOAP APIs, polymorphism, and exception handling, alongside classic DSA (data structures and algorithms) rounds — arrays, dynamic programming, recursion, and linked lists show up repeatedly across real reported interviews.

**Sample question set (technical):**
* Explain the difference between a class and an object in OOP, with an example
* What are SQL joins? Explain inner join vs outer join
* How would you optimize a slow-running SQL query?
* Explain polymorphism with a real example
* Walk me through how garbage collection works in a language of your choice
* What's the difference between REST and SOAP APIs?
* Given an array, find two numbers that add up to a target sum — explain your approach

**Sample question set (behavioral, SDE-specific):**
* Describe a time you worked in a team to solve a technical problem. What was your specific role?
* Tell me about a project you're proud of — what challenges did you face?
* Have you faced disagreements with teammates on a technical decision? How did you handle it?
* How do you manage tight deadlines across multiple tasks?

**Resume-tied pattern to replicate:** real interviewers frequently ask candidates to explain a listed project from scratch and rate their own familiarity with the technologies used in it — your Question Maker should replicate this exact pattern using whatever the resume actually says.

---

#### Data Analyst

Real data analyst interviews are structured around a predictable loop — a recruiter screen, a hiring manager/fit round, and a technical round focused on SQL — often followed by business-case reasoning. Interviewers commonly test statistics fundamentals like hypothesis testing, confidence intervals, p-values, and correlation vs. causation, plus hands-on data manipulation.

**Sample question set (technical):**
* Write a SQL query to find the top 10 customers by sales amount
* How would you handle missing or duplicate data in a dataset?
* Explain the difference between correlation and causation
* What's a p-value, and how would you explain it to a non-technical stakeholder?
* Describe how you'd merge two datasets with different schemas
* Which visualization would you use to show a trend over time, and why?

**Sample question set (business/problem-solving):**
* Sales dropped 25% last month — how would you investigate?
* What metrics would you use to measure whether a new feature is being adopted?
* How would you design an experiment to test if a change improved user engagement?

**Sample question set (behavioral):**
* Tell me about a time your analysis changed a business decision
* Describe a time you had to explain a technical finding to a non-technical audience

---

#### Frontend Developer

Real frontend interviews center on three layers — HTML/CSS fundamentals, JavaScript concepts (data types, the event loop, call stack, promises, async/await), and framework-specific questions like React hooks — and interviewers often push candidates to explain alternative approaches, not just one working solution.

**Sample question set (technical):**
* What's the difference between `div` and `span`? When would you use each?
* Explain the CSS box model
* What is event delegation in JavaScript, and why is it useful?
* Explain closures with an example
* What's the difference between `let` and `var`?
* What is the virtual DOM, and why does React use it?
* How would you make a webpage responsive across screen sizes?

**Sample question set (behavioral):**
* Tell me about your role and responsibilities in your last project/internship
* Describe a UI bug that was hard to track down — how did you solve it?

---

#### General HR / Behavioral (any role)

These are standard across almost every interview, regardless of role — used to assess fit, communication, and self-awareness rather than technical skill.
* Tell me about yourself
* What are your greatest strengths and weaknesses?
* Why do you want to work here / in this role?
* Describe a time you faced a conflict with a teammate — how did you resolve it?
* Tell me about a time you failed — what did you learn?
* How do you handle pressure or tight deadlines?
* Where do you see yourself in five years?
* Describe a time you had to adapt to a significant change

---

### Part C — How to Use This in the Question Maker Prompt

When prompting Antigravity for Step 4, include a note like this:
> "Here are sample real interview questions for [role]: [paste relevant section above]. Use these as a style reference — generate NEW questions in a similar style and difficulty, personalized using the resume data, rather than reusing these exact questions."

This keeps the AI's questions feeling authentic without just copying a fixed list every time.

---

## PART 3 — RESUME → QUESTION → GOOD ANSWER EXAMPLES

### Resume → Question → Good Answer Examples

This section pairs two real resumes with resume-specific questions and model "good" answers. Use this as a few-shot example in your Question Maker and Grading prompts — it shows Gemini exactly what a resume-tied question looks like, and what a strong answer looks like against the rubric.

---

### RESUME 1 — Mohd Mehraj

**Background:** CSE student, solo AI-product builder. Business development intern (built outbound sales from scratch, LinkedIn prospecting, 15-20% conversion to discovery calls). Built two Shopify stores end-to-end (Mazami, Sonali Jain) using AI-assisted tools, both lifting conversions/engagement ~40%. Built "The Signal," a solo RSS-to-LLM content curation app using Gemini Flash API. Skills: Claude Code, Antigravity, Shopify, WordPress, LinkedIn Sales Navigator.

#### Questions & Model Answers

**Q1. Walk me through the RSS-to-LLM filtering pipeline you built for "The Signal" using the Gemini Flash API. What were the key design decisions?**
> *Model Answer:* The pipeline pulls in RSS feeds, then passes each item through Gemini Flash with a prompt that filters for genuine relevance instead of just engagement-bait signals. The key decision was choosing Flash specifically for its speed and low cost, since filtering runs on every incoming item — a slower or pricier model wouldn't scale for constant filtering. I also designed it in modular stages, so I could test the filtering logic on its own before wiring in the rest of the pipeline, which let me iterate fast without breaking the whole system each time.

**Q2. Your Shopify build for Mazami lifted mobile conversions by 40%. What specific changes drove that?**
> *Model Answer:* The biggest lever was responsiveness — making sure the layout, image sizing, and checkout flow actually worked well on mobile screens instead of just scaling down a desktop design. I also focused on storytelling in the page structure so visitors connected with the brand narrative, not just a product grid, which tends to keep people engaged longer and reduces early drop-off before they even reach checkout.

**Q3. You used AI-assisted tools like Claude Code to build apps solo. Walk me through your actual workflow from idea to shipped product.**
> *Model Answer:* I start by scoping the smallest working version of the idea, then use Claude Code to build that core piece first rather than the whole system at once. I test that piece, fix what's broken, and only then move to the next module — shipping in stages instead of waiting for a "complete" version. This matters because AI-assisted development can generate a lot of code fast, but if you don't test incrementally, bugs stack up and get harder to isolate.

**Q4. You joined as the first sales hire at Diverse Lab. How did you build the outbound BD function from scratch with no existing playbook?**
> *Model Answer:* Situation: I joined as the company's first sales hire for an AI creative studio with no existing outreach process. Task: I needed to build a working pipeline that could consistently generate qualified leads. Action: I moved away from generic cold outreach and built peer-to-peer, industry-tailored sequences with portfolio-led proposals, sourcing 40+ leads weekly across the US, UK, UAE, and India through LinkedIn Sales Navigator. Result: This converted 15-20% of qualified conversations into discovery calls, which became the foundation of the company's ongoing pipeline.

**Q5. How do you decide when to ship an early, imperfect version of a product versus polishing it further?**
> *Model Answer:* I look at whether the core functionality actually works end-to-end, even roughly — if it does, I ship it and improve based on real usage rather than guessing what needs polish. With "The Signal," I deliberately built in modular stages so I could ship working pieces early and get feedback, instead of chasing a perfect plan that might not even match what actually turns out to matter.

**Q6. What technical trade-offs did you consider when choosing Gemini Flash specifically for your filtering pipeline?**
> *Model Answer:* The main trade-off was speed and cost versus raw reasoning quality. Flash is faster and cheaper, which matters a lot for a pipeline filtering many items regularly, but it's less capable than a larger model for deeply nuanced judgment calls. Since the filtering task is more about relevance-matching than complex reasoning, Flash's speed/cost advantage outweighed the smaller drop in reasoning depth for this specific use case.

**Q7. You manage both client-facing sales and hands-on development. How do you prioritize your time between the two?**
> *Model Answer:* I treat sales as time-sensitive and dev work as depth-sensitive — outreach and lead follow-ups have to happen on a schedule or momentum dies, so I protect blocks of time for that first. Development work I batch into longer, uninterrupted sessions since context-switching mid-build is costly. In practice, this meant handling BD in the mornings when leads are most responsive, and building in longer stretches later.

**Q8. Describe how you approached client discovery for the Sonali Jain luxury fashion store, and how that shaped your build.**
> *Model Answer:* I started by understanding the brand's existing identity and what made the label feel "luxury" beyond just the products — tone, visual language, and story. That shaped decisions like designing around storytelling elements rather than a standard product-grid template, which is part of why the build raised engagement and time on site by 35% while lowering bounce rate.

**Q9. If you had to scale "The Signal" to thousands of users, what would need to change architecturally?**
> *Model Answer:* Right now the pipeline likely processes feeds per-user or per-request; at scale, I'd move to a shared processing layer that filters common feed sources once and serves results to multiple users, instead of re-running the same Gemini call redundantly. I'd also add caching for frequently-seen articles and probably queue-based processing so a spike in feed volume doesn't slow down real-time delivery for active users.

**Q10. Tell me about a time your outreach approach didn't work, and what you changed.**
> *Model Answer:* Situation: Early on, I was using more generic outreach templates for leads. Task: I needed to actually convert qualified conversations into discovery calls, not just get replies. Action: I noticed generic messaging wasn't landing, so I shifted to peer-to-peer, industry-tailored sequences with portfolio-led proposals instead. Result: That specific shift is what took conversion from low response rates to converting 15-20% of qualified conversations into booked calls.

---

### RESUME 2 — Hammad Warsi

**Background:** Associate Product Manager at Paytm (payments/ecommerce, fintech). Previously Product Management Trainee at Telgoo5 (B2B ecommerce for telecom). Built a RAG-based AI support assistant (LangChain + GPT-4 + FAISS). Strong on KPIs, A/B testing, RBAC, RICE prioritization. Side projects: HireHub (job portal), Internal API Developer Portal, CryptoVesta dashboard, Olympics Medal Prediction ML model.

#### Questions & Model Answers

**Q1. Walk me through how you used SQL and Mixpanel to track KPIs like DAU and settlement TAT. What were you actually looking for?**
> *Model Answer:* I used SQL to pull raw transaction and settlement data directly from the database when I needed custom breakdowns Mixpanel's dashboards didn't cover, and Mixpanel for tracking user-level behavior like drop-off points in the checkout funnel. For settlement TAT specifically, I was looking for outlier delays that pointed to a bottleneck in reconciliation, not just the average — averages can hide the specific failure points that actually hurt merchants.

**Q2. You improved on-time feature delivery by 20% and reduced ambiguity-related rework by 30%. What specifically changed in your process?**
> *Model Answer:* The biggest change was tightening requirements before development started — writing clearer acceptance criteria during backlog grooming so engineers weren't making assumptions mid-sprint. I also ran more structured sprint planning sessions where edge cases got discussed upfront instead of surfacing as rework later. Ambiguity-driven rework usually comes from unclear requirements, not slow engineering, so fixing it earlier in the process had the bigger impact.

**Q3. Describe the RAG-based AI support assistant you built with LangChain, GPT-4, and FAISS. How did you evaluate it for hallucination rate and CSAT?**
> *Model Answer:* The assistant used FAISS for retrieving relevant support documents and GPT-4 to generate answers grounded in that retrieved context, which is what RAG is for — reducing hallucination by forcing the model to answer from real documents instead of pure generation. For evaluation, I built a framework that specifically flagged answers not traceable back to a retrieved source as potential hallucinations, and tracked CSAT scores from actual users to catch cases where answers were accurate but still unhelpful or poorly phrased.

**Q4. Walk me through an A/B test you ran to improve checkout completion rate. How did you design it and measure success?**
> *Model Answer:* I identified a specific friction point in the checkout flow through funnel analysis, then tested a variant against the existing flow with users randomly split between the two. Success was measured primarily by completion rate, but I also tracked transaction conversion as a secondary metric to make sure the change didn't just move people through faster without actually completing valid transactions. That test contributed to an 18% improvement in completion rate.

**Q5. You worked with compliance and risk teams to deliver RBI-compliant payment flows. Describe a time compliance requirements conflicted with product/UX goals.**
> *Model Answer:* Situation: Compliance required additional verification steps in certain payment flows for RBI compliance. Task: I needed to keep the checkout experience smooth while meeting those requirements. Action: I worked with the compliance team to understand which steps were strictly mandatory versus flexible in presentation, then redesigned the flow so mandatory checks felt like a natural part of the process rather than an interruption. Result: This let us stay compliant while keeping conversion impact minimal, since the added friction was placed where it felt expected rather than jarring.

**Q6. How did you prioritize features for HireHub using the RICE framework? Walk me through an example.**
> *Model Answer:* For HireHub, I scored candidate features like application tracking against Reach, Impact, Confidence, and Effort — for example, a resume-matching feature scored high on Impact and Reach since it affected both recruiters and candidates, but I weighed Effort against simpler wins like improving the application form flow first, since that had a faster path to improving the funnel with lower build cost.

**Q7. Tell me about a challenging cross-team dependency you had while building the Internal API Developer Portal. How did you resolve it?**
> *Model Answer:* Situation: Building the API portal required input from multiple teams who each owned different APIs, and getting consistent documentation from all of them was slow. Task: I needed standardized, discoverable documentation across teams with different priorities. Action: I defined a shared documentation template and pushed for each team to own filling in their section, rather than trying to centrally document every API myself. Result: This reduced cross-team dependency going forward, since teams could self-serve updates instead of routing every change through me.

**Q8. You reduced customer query resolution time by 40% with the RAG assistant. What were the main sources of latency or error you had to fix?**
> *Model Answer:* The biggest source of error early on was the retrieval step pulling loosely related documents instead of the most relevant one, which led to answers that sounded confident but weren't accurate. I improved this by refining how documents were chunked and indexed in FAISS, so retrieval matched more precisely. For latency, caching frequent queries and limiting retrieved context size to only what's necessary helped keep response times down without hurting accuracy.

**Q9. Describe your approach to managing sprint planning and backlog grooming. What makes a backlog well-groomed in your view?**
> *Model Answer:* A well-groomed backlog has each ticket written with clear acceptance criteria and known edge cases discussed before the sprint starts, not during it. My approach is to review upcoming tickets with engineers ahead of planning specifically to surface ambiguity early, since that's what usually causes rework — not the complexity of the work itself, but unclear expectations going in.

**Q10. Tell me about the Olympics Medal Prediction ML project. What features did you use, and how did you validate the 87% accuracy?**
> *Model Answer:* I used historical performance data — things like past medal counts, number of athletes per country, and host-country advantage — as input features for the model. For validation, I split the data into training and test sets so the accuracy reflected performance on unseen data, not just how well it fit data it had already seen, which is important since a model can look accurate on training data while still failing to generalize.

---

### How to Use This File
* **Paste Resume 1 or 2's Q&A block** into your Question Maker prompt as a few-shot example: *"Here's an example of good resume-tied questions for a similar background: [paste]."*
* **Paste model answers** into your Grading prompt as calibration examples of what a high-scoring answer looks like, so Gemini has a concrete reference point instead of just the rubric text alone.

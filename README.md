# EdTech Session Intelligence Pipeline

An LLM workflow that converts raw consultant session notes into CRM-ready discovery summaries.

**Results: 20 minutes of documentation cut to under 5 per session (75% reduction), validated across 100+ production sessions, 25%+ conversion rate on profiled leads.** Built and run in production during a high-touch EdTech sales role, February to April 2026. Runnable Python CLI included; also works with zero code in a Claude artifact.

---

## The Problem

EdTech consulting teams run hundreds of discovery sessions a month. Each one produces 20+ minutes of manual note-taking in whatever format the consultant prefers. The costs stack up:

- Note formats vary by consultant, so nobody downstream can scan them quickly
- New hires take weeks to learn what a high-intent lead actually looks like
- Intent signals get buried in narrative text, and follow-up opportunities die there

The team hired in weekly cohorts with a small bench of team leads supervising, so every hour spent on documentation or training multiplied across the org.

---

## The Solution

A four-stage workflow. AI generates the questioning framework, suggests follow-ups during the call, structures the notes afterward, and scores conversion readiness.

### Stage 1: AI generates the consultation blueprint

Claude/GPT-4 creates a 7-phase structured questioning framework with dynamic follow-ups keyed to lead objections and profile signals:

- Career gap identity triggers (homemakers, mid-career breaks)
- Wasted potential triggers (overqualified/underpaid)
- AI adoption anxiety (IT/BPO workers, fear of becoming outdated)
- Financial pressure and dependency pain
- Real vs. casual urgency differentiation

### Stage 2: AI refines the conversation in real time

During each 20-minute consultation, AI suggests contextual follow-up questions based on the lead's emerging profile (location, experience, education, goals), stated constraints (family, financial, timeline, identity blocks), objections raised (price doubts, "I can do it myself", stalling), and emotional pain points (isolation, burnout, helplessness).

### Stage 3: AI structures the raw notes

A Claude/GPT-4 artifact processes the unstructured session notes and outputs a structured candidate profile: 10+ key signals (location, experience, intent, timeline, constraints, urgency), specific talking points for the follow-up call, risk flags (blockers, dependencies, identity gaps), and consistent template formatting across every profile.

### Stage 4: AI analyzes conversion readiness

Each profile gets an intent score (HIGH/MEDIUM/LOW), a 1-line conversion explanation naming the primary driver or blocker, strength signals, and personalized talking points for handling objections.

The output lands in a copy-paste CRM format. Under 2 minutes to populate, no API integration required, no data stored in AI systems.

---

## Real Impact

| Metric | Result |
|--------|--------|
| Session processing time | 20 mins to under 5 mins (75% reduction) |
| Sessions validated | 100+ sessions personally operated and profiled |
| Conversion rate | 25%+ on profiled sessions |
| Training use | Framework adopted as reference material for new-hire onboarding |

Every number above comes from sessions I ran myself. The framework was shared as team training material; I have not audited adoption beyond my own cohort, so I don't claim numbers for it.

---

## How It Worked

### Input

Unstructured consultant notes (Q&A format, scattered details):

```
"Bangalore, 3 yrs DevOps, remote job converting to office, kids to manage,
wants work-life balance, 15 LPA current, 18–20 expected, 5–6 months timeline,
recent marriage, civil engineer husband, consistent best rating"
```

### Process

A Claude artifact with a custom prompt extracts profile data (location, experience, skills, education), surfaces intent signals (motivation, timeline, constraints, urgency), identifies risks and strengths, generates conversion talking points, and formats everything for copy-paste into the CRM.

### Output

```
DevOps Engineer – HIGH INTENT (3 yrs exp)
Location: Bangalore
Current: 15 LPA (Hybrid) | Expected: 18–20 LPA
Pain: Remote → office mandate | Constraint: Kids + work-life balance
Timeline: Ideal 5–6 months, early switch if opportunity (2-month notice)
Strength: Consistent best rating, already upskilling, structured mindset
Talk Track: Offer remote role + structured upskilling roadmap addressing family concerns
```

---

## Why This Matters

New consultants ramp faster because the profile library shows them what high intent looks like in real examples instead of abstract training slides. Structured data means fewer wasted follow-ups and better qualification. The system encodes 100+ real examples of high, medium, and low intent signals, so the team's judgment no longer depends on any one experienced consultant.

---

## Technical Architecture

Five discrete stages. Stages 1–2 use AI to prepare and guide the consultation; stages 3–5 process the output.

```
STAGE 1: CONSULTATION BLUEPRINT GENERATION
         └─ Claude generates 7-phase framework with dynamic
            follow-up questions keyed to objection type,
            emotional trigger, and lead profile signals

STAGE 2: REAL-TIME CONVERSATION REFINEMENT
         └─ AI suggests contextual follow-ups during the call
            based on emerging lead profile + stated constraints

STAGE 3: CONSULTANT CAPTURES RAW NOTES
         └─ Q&A responses, signals, pain points documented
            (any format: transcript, bullet notes, form)

STAGE 4: AI STRUCTURES OUTPUT + SCORES CONVERSION
         └─ process_session.py sends notes to Claude API →
            • JSON profile: 10+ signals extracted
            • Confidence score (0.0–1.0) per inference
            • Conversion readiness: HIGH / MEDIUM / LOW
            • Quality gate: scores <0.6 flagged for review
            • Talk track for follow-up call

STAGE 5: CRM ENTRY (HUMAN-CONTROLLED, <2 MINS)
         └─ Validated profile pushed to CRM via API or copy-paste
```

### API specifications

| Parameter | Value |
|---|---|
| Model | `claude-3-5-sonnet-20241022` (default) |
| Max tokens | 1,500 per session |
| Latency | 2–4 sec per profile |
| Cost per session | ~$0.05–0.10 (Sonnet pricing) |
| Throughput | ~20 sessions/conversation; batch mode for volume |
| Quality gate | Confidence < 0.6 → `REQUIRES_CLARIFICATION` flag, manual review |
| Error handling | Malformed JSON → retry + partial profile + flag |

### Execution options

| Method | Best for | Setup time |
|---|---|---|
| `process_session.py` (CLI) | Developers, local testing | ~5 min |
| n8n / Make webhook | Ops teams, automated pipelines | ~30 min |
| Claude artifact (no-code) | Consultants without API access | 0 min |

Privacy note: AI processes notes in-context only. No data is stored in AI systems. All profiles remain in your CRM or local files.

---

## Known Limitations

### Hallucination pattern

Claude occasionally assumes missing lead data and asks clarification questions even after details were given.

- Trigger: sparse or ambiguous notes
- Behavior: asks "Can you clarify X?" when X was already mentioned
- Workaround: keep notes detailed; start a new conversation every ~20 leads (context window accumulation slows responses after that)

### Scaling

The workflow handles about 20 candidate profiles per conversation cleanly. After that, response time increases as the context window saturates. The fix is simple: batch leads into separate conversations, 20 leads per session.

---

## What's Included

| File | Purpose |
|---|---|
| `README.md` | Workflow overview, metrics, architecture, limitations |
| `process_session.py` | Runnable Python CLI: single session + batch mode, quality gate, CRM stub |
| `requirements.txt` | `anthropic`, `python-dotenv` |
| `.env.example` | Environment variable template (API key, model, thresholds) |
| `system-prompt.md` | Full Claude system prompt + psychology framework + JSON schema |
| `sample-output.json` | 2 annotated production examples with confidence scoring |
| `CONSULTATION_BLUEPRINT_INTEGRATION.md` | 7-phase consultation framework: how AI generates the blueprint |
| `COPY_PASTE_TEMPLATE.md` | CRM entry format for no-code/manual use |
| `REAL_EXAMPLES_BEFORE_AFTER.md` | 10 real before/after profiles (raw notes → structured output) |
| `CONVERSION_ANALYSIS.md` | Intent scoring + 1-line conversion explanation for all 10 examples |
| `IMPLEMENTATION_GUIDE.md` | Step-by-step integration for CLI, n8n, Make, Zapier, HubSpot, Salesforce |

---

## For Your Use

1. Copy the system prompt into a Claude artifact or GPT-4 custom instructions
2. Paste raw session notes
3. Copy the structured summary into your CRM

That's the whole loop. No API, no webhooks, no data storage. To adapt it for another domain, replace the candidate signals with your own (customer profiles, patient intake, sales leads). The pattern transfers.

---

## Author

**Saurabh Sarkar**
AI Workflow Automation & Sales Operations
[saurabhsarkar.7397@gmail.com](mailto:saurabhsarkar.7397@gmail.com)

Built with Claude and GPT-4 artifacts. Validated across 100+ sessions I personally operated, February to April 2026. Open-source under MIT; adapt it to any consultative sales domain.

# EdTech Session Intelligence Pipeline

**Production-validated LLM workflow that structured session notes into CRM-ready discovery summaries for high-touch consulting sales.**

---

## The Problem

EdTech consulting teams conduct hundreds of sessions monthly. Each produces:
- **20+ minutes of manual note-taking** (unstructured, scattered)
- **Inconsistent formatting** (different consultants, different styles)
- **Training overhead** (50+ new hires weekly = 4–6 week ramp time to sales velocity)
- **Conversion leakage** (intent signals buried in messy notes, follow-up opportunities missed)

**Hiring scale:** 50+ candidates/week × supervision by 5–6 team leads = **training costs bottleneck**

---

## The Solution

**Four-Stage AI-Powered Workflow** – AI generates the framework, refines the conversation in real-time, structures the output, and analyzes conversion readiness.

### Stage 1: AI Generates the Consultation Blueprint
Claude/GPT-4 creates a **7-phase structured questioning framework** with dynamic follow-ups tailored to lead objections and profile signals:
- Career gap identity triggers (homemakers, mid-career breaks)
- Wasted potential triggers (overqualified/underpaid)
- AI adoption anxiety (IT/BPO workers, outdatedness fear)
- Financial pressure & dependency pain
- Real vs. casual urgency differentiation

### Stage 2: AI Refines Conversation In Real-Time
During each 20-minute consultation, AI suggests **contextual follow-up questions** based on:
- Lead's emerging profile (location, experience, education, goals)
- Stated constraints (family, financial, timeline, identity blocks)
- Objections raised (price doubts, "I can do it myself", stalling indicators)
- Emotional pain points discovered (isolation, burnout, helplessness)

### Stage 3: AI Structures the Raw Notes
Claude/GPT-4 Artifact processes unstructured session notes and outputs:
- **Structured candidate profiles** (10+ key signals: location, experience, intent, timeline, constraints, urgency)
- **Conversion hooks** (specific talking points for follow-up calls)
- **Template-based formatting** (consistent across all 500+ profiles)
- **Risk flags** (blockers, dependencies, identity gaps)

### Stage 4: AI Analyzes Conversion Readiness
Each profile includes:
- **Intent scoring** (HIGH/MEDIUM/LOW)
- **1-line conversion explanation** (primary driver or blocker, e.g., "Financial pressure outweighs family constraints—high urgency")
- **Strength signals** (consistent performance, mindset, adaptability)
- **Talking points** (personalized hooks for overcoming objections)

**Copy-paste CRM format** (ready for manual entry, <2 mins to populate)

**No API integration. No data stored in AI. No JSON schema hassle. Just: Blueprint → Questions → Notes → Structure → Analysis → Copy to CRM.**

---

## Real Impact

| Metric | Result |
|--------|--------|
| **Session processing time** | 20 mins → <5 mins (**75% reduction**) |
| **Training cost savings** | All candidates trained on GPT + system became reference framework |
| **Framework adoption** | 500+ consultants trained on the system (team-wide rollout) |
| **Sessions validated** | 100+ sessions personally operated & profiled (production accuracy baseline) |
| **Conversion lift** | ~**25%** (better signal extraction = better targeting) |

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
Claude Artifact processes through custom prompt that:
- Extracts profile data (location, exp, skills, education)
- Surfaces intent signals (motivation, timeline, constraints, urgency)
- Identifies risks & strength signals
- Generates conversion talking points
- Formats for copy-paste into CRM

### Output
Structured summary (copy-paste ready):
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

1. **Faster onboarding:** New consultants ramp 50% faster (see what high-intent *looks like* in real examples)
2. **Better qualification:** Structured data → fewer wasted follow-ups → higher conversion
3. **Institutional memory:** System encodes 100+ real examples of high/medium/low intent signals
4. **Training cost reduction:** Framework becomes reference material for all new cohorts
5. **Scalable knowledge:** Not dependent on any one "superstar" consultant's judgment

---

## Technical Architecture

Five discrete stages. Stages 1–2 use AI to prepare and guide the consultation; Stages 3–5 process the output.

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

### API Specifications

| Parameter | Value |
|---|---|
| **Model** | `claude-3-5-sonnet-20241022` (default) |
| **Max tokens** | 1,500 per session |
| **Latency** | 2–4 sec per profile |
| **Cost per session** | ~$0.05–0.10 (Sonnet pricing) |
| **Throughput** | ~20 sessions/conversation; batch mode for volume |
| **Quality gate** | Confidence < 0.6 → `REQUIRES_CLARIFICATION` flag, manual review |
| **Error handling** | Malformed JSON → retry + partial profile + flag |

### Execution Options

| Method | Best for | Setup time |
|---|---|---|
| `process_session.py` (CLI) | Developers, local testing | ~5 min |
| n8n / Make webhook | Ops teams, automated pipelines | ~30 min |
| Claude Artifact (no-code) | Consultants without API access | 0 min |

**Privacy-first:** AI processes notes in-context only. No data stored in AI systems. All profiles remain in your CRM or local files.

---

## Known Limitations

### Hallucination Pattern
Claude occasionally **assumes missing lead data** and asks clarification questions even after details given.

- **Trigger:** Sparse or ambiguous notes
- **Behavior:** Asks "Can you clarify X?" when X was already mentioned
- **Workaround:** Keep notes detailed; start new conversation every ~20 leads (context window accumulation slows responses after that)

### Scaling
- **Seamless:** ~20 candidate profiles per conversation
- **After 20:** Response time increases (token context saturation)
- **Solution:** Batch leads into separate conversations (20 leads = 1 session)

---

## What's Included

| File | Purpose |
|---|---|
| `README.md` | Workflow overview, metrics, architecture, limitations |
| `process_session.py` | **Runnable Python CLI** — single session + batch mode, quality gate, CRM stub |
| `requirements.txt` | `anthropic`, `python-dotenv` |
| `.env.example` | Environment variable template (API key, model, thresholds) |
| `system-prompt.md` | Full Claude system prompt + psychology framework + JSON schema |
| `sample-output.json` | 2 annotated production examples with confidence scoring |
| `CONSULTATION_BLUEPRINT_INTEGRATION.md` | 7-phase consultation framework — how AI generates the blueprint |
| `COPY_PASTE_TEMPLATE.md` | CRM entry format for no-code/manual use |
| `REAL_EXAMPLES_BEFORE_AFTER.md` | 10 real before/after profiles (raw notes → structured output) |
| `CONVERSION_ANALYSIS.md` | Intent scoring + 1-line conversion explanation for all 10 examples |
| `IMPLEMENTATION_GUIDE.md` | Step-by-step integration for CLI, n8n, Make, Zapier, HubSpot, Salesforce |

---

## For Your Use

1. Copy system prompt into Claude Artifact or GPT-4 Custom Instructions
2. Paste raw session notes
3. Copy structured summary into CRM
4. That's it. No API, no webhooks, no data storage.

**Adapt for your domain:** Replace candidate signals with your domain (customer profiles, patient intake, leads, etc). Pattern is replicable.

---

## What This Shows for Portfolio

✅ **Real LLM integration in production** (not toy examples)  
✅ **Measurable business impact** (75% time savings, 25% conversion lift; 500+ consultants trained, 100+ sessions validated)  
✅ **Scalable pattern** (production-validated across 100+ sessions; framework adopted by entire team)  
✅ **Thoughtful constraints** (hallucination mitigations, privacy-first, knows scaling limits)  
✅ **End-to-end thinking** (problem → solution → known tradeoffs → honest limitations)

---

## Author

**Saurabh Sarkar**  
AI Workflow Automation & Sales Operations  
[saurabhsarkar.7397@gmail.com](mailto:saurabhsarkar.7397@gmail.com)

**Built with:** Claude + GPT-4 Artifacts  
**Validated:** 100+ sessions personally operated; framework adopted by 500+ team consultants, 2024–2025  
**Replicable:** Any consultative sales domain

*May 2026 — Production-validated, domain-agnostic, open-source*

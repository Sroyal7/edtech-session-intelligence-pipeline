# CRM Copy-Paste Template: EdTech Session Intelligence Pipeline

Use this exact template format to enter structured candidate profiles into your CRM. Copy the structured candidate block directly – no reformatting needed. <2 minutes per entry.

---

## Template Format

```
[ROLE] – [INTENT] INTENT ([YEARS] yrs exp)
Location: [CITY]
Current: [CURRENT_LPA] LPA ([CURRENT_STATUS]) | Expected: [EXPECTED_LPA] LPA
Pain: [PRIMARY_CONSTRAINT] | Constraint: [SECONDARY_CONSTRAINTS]
Timeline: [IDEAL_TIMELINE], [FLEXIBILITY_NOTE]
Strength: [KEY_STRENGTH_1], [KEY_STRENGTH_2], [PATTERN_NOTE]
Talk Track: [SPECIFIC_TALKING_POINT_1] + [SPECIFIC_TALKING_POINT_2]
```

---

## Field Definitions & Placeholders

### [ROLE]
Candidate's professional role/title.
*Examples:* DevOps Engineer, QA Automation, Data Engineer, Backend Developer

### [INTENT]
Intent scoring from session.
*Values:* HIGH | MEDIUM | LOW

### [YEARS]
Years of professional experience (total).
*Format:* Number only (e.g., 3, 5, 7)

### [CITY]
Geographic location of candidate.
*Format:* City name, optionally state if relevant
*Examples:* Bangalore, Chennai, Hyderabad, Mumbai

### [CURRENT_LPA]
Current base salary in LPA (Lakhs Per Annum).
*Format:* Numeric range if provided (e.g., 15, 15–16, 14–16)
*Note:* If unknown, write "Not mentioned"

### [CURRENT_STATUS]
Work arrangement type.
*Values:* Remote | Hybrid | Office | On-site | Contract
*Format:* Single status or "Hybrid (3 days office, 2 remote)"

### [EXPECTED_LPA]
Target salary range in LPA.
*Format:* Range preferred (e.g., 18–20, 20–24)

### [PRIMARY_CONSTRAINT]
The main factor driving the switch (usually the pain point).
*Examples:*
- "Office mandate coming (5-day)"
- "Growth ceiling in current role"
- "Lack of work-life balance"
- "Remote-to-office conversion"
- "Relocation required by spouse"

### [SECONDARY_CONSTRAINTS]
Additional constraints affecting the candidate.
*Examples:*
- "Kids (5, 7) + family priorities"
- "Work-life balance non-negotiable"
- "Spouse in career transition"
- "Geographic constraints"
- "Requires learning opportunity"

### [IDEAL_TIMELINE]
Expected timeline for the switch.
*Format:* Duration or month range (e.g., "5–6 months", "Next 3 months", "ASAP")

### [FLEXIBILITY_NOTE]
Candidate's flexibility around timeline.
*Examples:*
- "Early switch possible if right opportunity"
- "2-month notice period"
- "Hard deadline: can't extend beyond Aug"
- "Flexible; no rush"

### [KEY_STRENGTH_1], [KEY_STRENGTH_2]
Distinguishing positive signals about the candidate.
*Examples:*
- "Consistent best rating from managers"
- "Already upskilling (AWS cert)"
- "Project ownership mindset"
- "Leadership potential"
- "Referral quality; no red flags"

### [PATTERN_NOTE]
Summary of the candidate's working/growth pattern.
*Examples:*
- "Structured, ownership-focused approach"
- "Self-directed learner"
- "Drives process improvement"
- "Cross-functional collaborator"

### [SPECIFIC_TALKING_POINT_1], [SPECIFIC_TALKING_POINT_2]
Exactly two talking points for follow-up call. Must be **specific to this candidate's constraints**, not generic.
*Format:* Action + benefit that addresses their specific pain/constraint

---

## Real Examples (Copy-Paste Ready)

### Example 1: High Intent – Ready to Call
```
DevOps Engineer – HIGH INTENT (3 yrs exp)
Location: Bangalore
Current: 15 LPA (Hybrid) | Expected: 18–20 LPA
Pain: Office mandate (5-day coming) | Constraint: Kids (5, 7) + work-life balance
Timeline: Ideal 5–6 months, early switch if opportunity
Strength: Consistent best rating, actively upskilling (AWS cert), structured mindset
Talk Track: Lead with remote-first role + structured upskilling pathway for growth. Frame as: "2-day office hybrid + remote-capable projects. Let's design a 6-month growth plan that doesn't compromise family time."
```

### Example 2: Medium Intent – Exploratory
```
QA Engineer – MEDIUM INTENT (4 yrs exp)
Location: Chennai
Current: 12 LPA (Office) | Expected: 14–16 LPA
Pain: Growth ceiling in current company | Constraint: Exploring options, family relocating
Timeline: Flexible, exploring for 2–3 months
Strength: Consistent high performer, process-focused, recently mentored junior team member
Talk Track: Emphasize structured learning path + mentorship opportunities. Position as: "We're building a scaled QA practice – your mentorship background is exactly what we need, with clear IC→Lead progression."
```

### Example 3: Low Intent – Hold for Now
```
Backend Developer – LOW INTENT (2 yrs exp)
Location: Hyderabad
Current: 10 LPA (Office) | Expected: 12–14 LPA
Pain: Not mentioned | Constraint: Recently hired (3 months), vague about next move
Timeline: Not mentioned
Strength: Not mentioned | Pattern: Needs more context
Talk Track: Too early; follow-up in 6 months. Current: "We think you're a great engineer – let's stay in touch as you settle in. We'll reach out in 6 months when you've got more clarity on next move."
```

---

## CRM Entry Workflow

1. **After session** (while notes are fresh): Paste raw consultant notes into Claude/GPT-4
2. **Get structured output:** Claude returns candidate profile in copy-paste template format
3. **Copy to CRM:** Select entire candidate block → Copy → Paste into CRM candidate record
4. **Verify formatting:** Check that no reformatting happened (should be clean copy-paste)
5. **Add follow-up task:** Set 5-day follow-up call reminder based on timeline/intent
6. **Log**: Add session date + talking point summary to notes

**Time per candidate:** <2 minutes after first session processing

---

## Field Mapping by CRM System

### HubSpot Contacts
- Name: From session notes or external source
- Job Title: [ROLE]
- Company: [From notes]
- Phone: [From notes]
- Notes: [Paste entire copy-paste template]
- Custom Fields:
  - Current_LPA: [CURRENT_LPA]
  - Expected_LPA: [EXPECTED_LPA]
  - Intent_Score: [INTENT]
  - Timeline: [IDEAL_TIMELINE]

### Salesforce Leads
- Title: [ROLE] – [INTENT] INTENT
- Company: [From notes]
- Phone: [From notes]
- Description: [Paste entire copy-paste template]
- Custom Fields:
  - Current_Compensation__c: [CURRENT_LPA]
  - Expected_Compensation__c: [EXPECTED_LPA]
  - Intent_Score__c: [INTENT]
  - Key_Constraint__c: [PRIMARY_CONSTRAINT]

### Generic CRM / Airtable
- Create one record per candidate
- Field 1 – Name
- Field 2 – Role: [ROLE]
- Field 3 – Profile (long text): [Paste entire copy-paste template]
- Field 4 – Intent: [INTENT]
- Field 5 – Next Follow-Up: [Date based on timeline]

---

## Tips for Accuracy

1. **Copy exactly.** Don't paraphrase or shorten. System relies on consistent format.
2. **Fill every field.** If a signal isn't mentioned, write "Not mentioned" – don't leave blank.
3. **Make talking points specific.** Generic points (e.g., "Growth opportunity") waste follow-up calls. Match to their actual constraint.
4. **Timeline is critical.** It determines follow-up schedule. If vague, note that.
5. **Strength signals predict conversion.** A candidate with strong signals + clear timeline = 5/5 call-readiness.

---

## Quality Checklist Before CRM Entry

- [ ] All 12 fields filled (or marked "Not mentioned")
- [ ] Talking points are specific to this candidate, not generic
- [ ] Intent score matches timeline + constraint + strength signals
- [ ] Location, compensation, timeline are factually accurate from notes
- [ ] No typos or formatting issues
- [ ] Template format unchanged (copy-paste compatible)

---

*Template Version: May 2026 – Production-Validated*
*Validated across 100+ candidate sessions, February to April 2026*
*CRM integrations: HubSpot, Salesforce, Airtable, generic systems*

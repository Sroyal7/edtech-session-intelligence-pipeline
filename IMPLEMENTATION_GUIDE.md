# Implementation Guide: EdTech Session Intelligence Pipeline

This guide walks you through deploying this documentation system in your own environment—from local testing to production CRM integration.

---

## Prerequisites

- Claude API key (from [console.anthropic.com](https://console.anthropic.com))
- Python 3.8+ (for CLI) OR webhook-capable platform (n8n, Make, Zapier)
- CRM access (HubSpot, Salesforce, Pipedrive, or custom API)
- ~30 minutes for initial setup

---

## Option A: Local CLI (Python)

### Step 1: Environment Setup

```bash
# Clone this repo
git clone https://github.com/YOUR_USERNAME/edtech-session-intelligence-pipeline.git
cd edtech-session-intelligence-pipeline

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install anthropic python-dotenv

# Create .env file
cat > .env << EOF
ANTHROPIC_API_KEY=sk-ant-...
SKILL_PLATFORM_NAME="Your Skill Platform Name"
EOF
```

### Step 2: Process a Session (Python)

```python
from anthropic import Anthropic

client = Anthropic()

# Read the system prompt
with open("system-prompt.md", "r") as f:
    system_prompt = f.read()

# Raw session notes from your consultant
raw_notes = """
Prospect: Rajesh, 28, IT background. Interested in data analytics bootcamp.
Asked about job placement and time commitment. Concerned about price ($800).
We discussed ROI—he said senior data engineers at his company make 3x his salary.
Agreed to review curriculum and call back in 7 days.
"""

# Call Claude
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",  # or claude-3-opus-20240229
    max_tokens=1024,
    system=system_prompt,
    messages=[
        {
            "role": "user",
            "content": f"Process these session notes:\n\n{raw_notes}"
        }
    ]
)

# Extract JSON from response
import json
output = json.loads(response.content[0].text)
print(json.dumps(output, indent=2))
```

### Step 3: Push to CRM

```python
import requests

# Example: HubSpot
hubspot_api_key = "YOUR_HUBSPOT_API_KEY"
contact = {
    "properties": {
        "firstname": output["prospect"]["name"],
        "email": output["prospect"]["email"],
        "phone": output["prospect"]["phone"],
        "hs_lead_status": "MQL",  # Map from output["conversion_signals"]["readiness_to_enroll"]
    }
}

response = requests.post(
    "https://api.hubapi.com/crm/v3/objects/contacts",
    json=contact,
    headers={"Authorization": f"Bearer {hubspot_api_key}"},
)
```

---

## Option B: Webhook-Based (n8n / Make)

### For n8n (Self-Hosted or Cloud)

1. **Create a new workflow**
2. **Add trigger:** HTTP webhook (receives raw session notes as JSON or text)
3. **Add step:** Call Anthropic API via HTTP request
   ```
   POST https://api.anthropic.com/v1/messages
   Headers:
     x-api-key: YOUR_ANTHROPIC_API_KEY
     content-type: application/json
   Body:
     {
       "model": "claude-3-5-sonnet-20241022",
       "max_tokens": 1024,
       "system": "[COPY SYSTEM PROMPT HERE]",
       "messages": [
         { "role": "user", "content": "{{ $json.raw_notes }}" }
       ]
     }
   ```
4. **Add step:** Parse JSON response
5. **Add step:** Create HubSpot contact (or your CRM API)
6. **Test:** Send sample raw notes to webhook

### For Make (formerly Integromat)

1. **Create new scenario**
2. **Trigger:** Webhook (receives raw_notes)
3. **Module 1:** HTTP request to Anthropic API (same as n8n above)
4. **Module 2:** JSON parser
5. **Module 3:** HubSpot Create Contact (or your CRM)
6. **Test & activate**

---

## Option C: Zapier (No-Code)

1. **Create Zap**
2. **Trigger:** Email or webhook (raw session notes)
3. **Action 1:** Custom request to Anthropic API
4. **Action 2:** Parse JSON
5. **Action 3:** Create HubSpot contact

(Note: Zapier's free tier has rate limits; consider n8n or Make for high volume.)

---

## Session Input Formats

### Format 1: Raw Transcript

```
Prospect: Vikas, 24, Engineering degree. Called to ask about data science bootcamp.
Wants to transition from hardware to software. Main concern: will bootcamp get him job offers?
I explained placement rate is 85%, showed 3 alumni case studies. He seemed convinced.
Agreed to attend live demo class tomorrow. Email: vikas.m@email.com
```

### Format 2: Structured Form

```json
{
  "prospect_name": "Vikas",
  "prospect_email": "vikas.m@email.com",
  "age_approx": "24",
  "background": "Engineering degree, 6 months software experience",
  "skill_interest": "data science",
  "questions_asked": [
    "What's the job placement rate?",
    "Can I do this while freelancing?"
  ],
  "key_objection": "Cost seems high",
  "objection_addressed": "Shared ROI (₹3L salary jump in 18 months)",
  "next_step": "Demo class tomorrow at 7 PM"
}
```

### Format 3: Call Transcript (Parsed)

```
[00:15] Prospect asked about course duration
[00:45] Expressed concern about job market relevance
[02:10] We discussed alumni outcomes
[03:00] Prospect asked about refund policy
[03:45] Prospect committed to trial class
```

All formats work; the system prompt is flexible enough to parse any of these.

---

## CRM Integration Examples

### HubSpot Integration

```python
def push_to_hubspot(output_json, api_key):
    import requests
    
    prospect = output_json["prospect"]
    conversion = output_json["conversion_signals"]
    follow_up = output_json["follow_up"]
    
    # Create/update contact
    contact_data = {
        "properties": {
            "firstname": prospect["name"].split()[0],
            "email": prospect["email"],
            "phone": prospect["phone"],
            "hs_lead_status": {
                "ready": "MQL",
                "considering": "MQL",
                "early-stage": "SAL",
                "not-ready": "BAT"
            }[conversion["readiness_to_enroll"]],
            "lifecyclestage": "lead",
            "custom_skill_interest": prospect["skill_interest"],
            "hs_lead_status": conversion["final_status"],
        }
    }
    
    # Create deal if "converted"
    if conversion["final_status"] == "converted":
        deal_data = {
            "properties": {
                "dealname": f"{prospect['name']} - {prospect['skill_interest']}",
                "dealstage": "negotiation",
                "amount": "0",  # Add actual pricing if available
            }
        }
        # POST to /crm/v3/objects/deals
    
    # Add activity/note with follow-up actions
    activity_data = {
        "engagement": {
            "type": "note",
            "body": follow_up["suggested_action"]
        }
    }
    
    return contact_data
```

### Generic Webhook (Zapier / Make / Custom)

```
POST {YOUR_CRM_WEBHOOK}
Content-Type: application/json

{
  "event": "prospect_documented",
  "prospect": {
    "name": "...",
    "email": "...",
    "phone": "..."
  },
  "conversion_signal": "considering",
  "follow_up_action": "...",
  "timestamp": "2026-05-10T16:45:00Z"
}
```

---

## Monitoring & Error Handling

### Common Issues

**Issue 1: Confidence scores are low (<0.5)**
- Claude is uncertain about the input data
- **Action:** Flag for manual review before CRM entry
- **Solution:** Provide clearer input (transcript > form > raw notes)

**Issue 2: JSON parsing errors**
- Response is not valid JSON
- **Action:** Add error handler in your pipeline
- **Solution:** Increase `max_tokens` in API call (default 1024 may be too low)

**Issue 3: Missing clarification flags**
- Response has "REQUIRES_CLARIFICATION" fields
- **Action:** Queue for human review before CRM push
- **Solution:** Don't auto-sync these prospects; let consultant review

### Logging & Monitoring

```python
import logging
from datetime import datetime

logging.basicConfig(
    filename=f"documentation_pipeline_{datetime.now().strftime('%Y%m%d')}.log",
    level=logging.INFO
)

def log_session(prospect_name, status, confidence, error=None):
    message = f"{datetime.now()} | {prospect_name} | {status} | confidence={confidence}"
    if error:
        message += f" | ERROR: {error}"
    logging.info(message)
```

---

## Performance Tuning

| Metric | Baseline | Target | Notes |
|---|---|---|---|
| **API latency** | 2–3 sec | <2 sec | Use faster model or cache system prompt |
| **Cost per session** | $0.08–0.12 | <$0.05 | Use Claude Sonnet instead of Opus |
| **Failure rate** | <1% | <0.1% | Improve input quality, increase confidence threshold |
| **Manual review rate** | 5–10% | <2% | Refine system prompt with platform-specific examples |

### Cost Optimization

- Use **Claude 3.5 Sonnet** (cheaper, faster) instead of Opus for volume
- Cache the system prompt if calling API repeatedly (see Anthropic docs)
- Batch process: collect 10 sessions, process in parallel

---

## Deployment Checklist

- [ ] API key configured securely (environment variable, not hardcoded)
- [ ] System prompt customized for your skill platform
- [ ] Test with 3–5 real session examples before production
- [ ] CRM webhook/API credentials configured
- [ ] Error handling in place (malformed input, missing fields)
- [ ] Logging enabled for audit trail
- [ ] Confidence threshold set (default 0.6 recommended)
- [ ] Team trained on "REQUIRES_CLARIFICATION" manual review process
- [ ] Monitor for 1 week; adjust prompt if manual review rate > 10%

---

## Next Steps

1. **Week 1:** Local testing with 5–10 real sessions
2. **Week 2:** Deploy to staging (n8n / Make test environment)
3. **Week 3:** Production deployment (monitor manual review rate)
4. **Week 4:** Optimize based on volume + error patterns

---

## Support & Customization

**Questions?**
- The system prompt is the main lever for customization. Adjust the JSON schema and prompt instructions for your specific platform.
- Common customizations: date formats, currency, skill categories, CRM field mappings.

**For production scaling:**
- Consider fine-tuning a smaller model on your platform's session data (requires 100+ examples)
- Add rate limiting if processing >100 sessions/day

---

*Last updated: May 2026*
*Version: 1.0*

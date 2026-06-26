"""
EdTech Session Intelligence Pipeline
process_session.py

Converts raw consultant session notes into structured JSON prospect profiles
using Claude. Supports single session processing and batch mode.

Usage:
    # Single session (interactive)
    python process_session.py

    # Single session (from file)
    python process_session.py --input notes.txt --output profile.json

    # Batch mode (folder of .txt files)
    python process_session.py --batch ./sessions/ --output-dir ./profiles/

Requirements:
    pip install -r requirements.txt
"""

import os
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import anthropic

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("MODEL", "claude-3-5-sonnet-20241022")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1500"))
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.6"))
PLATFORM_NAME = os.getenv("PLATFORM_NAME", "EdTech Platform")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            f"pipeline_{datetime.now().strftime('%Y%m%d')}.log"
        ),
    ],
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Load system prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT_PATH = Path(__file__).parent / "system-prompt.md"


def load_system_prompt() -> str:
    """Read system-prompt.md and extract the raw prompt block."""
    if not SYSTEM_PROMPT_PATH.exists():
        raise FileNotFoundError(
            f"system-prompt.md not found at {SYSTEM_PROMPT_PATH}. "
            "Make sure it is in the same directory as this script."
        )
    content = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    # Extract the content inside the first ```...``` block after "## System Prompt for Claude"
    in_block = False
    lines = []
    for line in content.splitlines():
        if "## System Prompt for Claude" in line:
            in_block = True
            continue
        if in_block:
            if line.strip().startswith("```") and not lines:
                continue  # opening fence
            elif line.strip() == "```" and lines:
                break      # closing fence
            else:
                lines.append(line)
    if lines:
        return "\n".join(lines).strip()
    log.warning("Could not extract prompt block from system-prompt.md; using full file.")
    return content


# ---------------------------------------------------------------------------
# Core processing
# ---------------------------------------------------------------------------

def process_session(raw_notes: str, client: anthropic.Anthropic) -> dict:
    """
    Send raw session notes to Claude and return parsed JSON profile.

    Args:
        raw_notes: Unstructured consultant notes (any format).
        client: Anthropic client instance.

    Returns:
        Parsed JSON dict. May contain 'clarification_needed' flags.

    Raises:
        ValueError: If Claude returns non-JSON or malformed output.
    """
    system_prompt = load_system_prompt()
    log.info("Sending session to Claude (%s, max_tokens=%d)", MODEL, MAX_TOKENS)

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": f"Process these session notes:\n\n{raw_notes}",
            }
        ],
    )

    raw_output = response.content[0].text.strip()

    # Strip markdown fences if Claude wraps output in ```json ... ```
    if raw_output.startswith("```"):
        lines = raw_output.splitlines()
        raw_output = "\n".join(
            line for line in lines if not line.strip().startswith("```")
        )

    try:
        profile = json.loads(raw_output)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Claude returned non-JSON output. Raw response:\n{raw_output}"
        ) from exc

    return profile


# ---------------------------------------------------------------------------
# Quality gate
# ---------------------------------------------------------------------------

def quality_gate(profile: dict) -> tuple:
    """
    Check profile against confidence threshold and clarification flags.

    Returns:
        (passes: bool, issues: list[str])
    """
    issues = []

    try:
        confidence = profile["session_summary"]["interest_signals"]["confidence"]
        if confidence < CONFIDENCE_THRESHOLD:
            issues.append(
                f"Confidence {confidence} below threshold {CONFIDENCE_THRESHOLD} "
                "-- manual review required."
            )
    except KeyError:
        issues.append("Missing confidence score in output.")

    clarification = profile.get("follow_up", {}).get("clarification_needed")
    if clarification:
        for flag in clarification:
            issues.append(f"REQUIRES_CLARIFICATION: {flag}")

    return len(issues) == 0, issues


# ---------------------------------------------------------------------------
# CRM push (stub -- replace with your CRM API)
# ---------------------------------------------------------------------------

def push_to_crm(profile: dict) -> bool:
    """
    Push structured profile to CRM system.
    Replace this stub with your actual integration (HubSpot, Salesforce, etc.).
    See IMPLEMENTATION_GUIDE.md for full examples.

    Returns True if push succeeded, False otherwise.
    """
    prospect = profile.get("prospect", {})
    conversion = profile.get("conversion_signals", {})

    log.info(
        "CRM push: %s | readiness=%s | status=%s",
        prospect.get("name", "Unknown"),
        conversion.get("readiness_to_enroll", "unknown"),
        conversion.get("final_status", "unknown"),
    )

    # --- REPLACE BELOW WITH YOUR CRM INTEGRATION ---
    # import requests
    # r = requests.post(
    #     "https://api.hubapi.com/crm/v3/objects/contacts",
    #     json={"properties": {"firstname": prospect.get("name"), ...}},
    #     headers={"Authorization": f"Bearer {os.getenv('CRM_API_KEY')}"},
    # )
    # return r.status_code == 201
    # -----------------------------------------------

    log.info("CRM stub active -- wire up push_to_crm() for your system.")
    return True


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def read_notes(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_profile(profile: dict, path: str) -> None:
    Path(path).write_text(
        json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    log.info("Profile saved to %s", path)


# ---------------------------------------------------------------------------
# CLI modes
# ---------------------------------------------------------------------------

def run_single(input_path, output_path, client):
    if input_path:
        raw_notes = read_notes(input_path)
        log.info("Loaded notes from %s", input_path)
    else:
        print("Paste raw session notes below. Press Enter twice when done:\n")
        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        raw_notes = "\n".join(lines).strip()

    if not raw_notes:
        log.error("No input provided.")
        return

    profile = process_session(raw_notes, client)
    passes, issues = quality_gate(profile)

    if not passes:
        log.warning("Quality gate FAILED:")
        for issue in issues:
            log.warning("  - %s", issue)
        profile["_quality_flags"] = issues
        log.warning("Profile flagged for manual review before CRM push.")
    else:
        push_to_crm(profile)

    if output_path:
        write_profile(profile, output_path)
    else:
        print("\n--- Structured Profile ---")
        print(json.dumps(profile, indent=2, ensure_ascii=False))


def run_batch(input_dir, output_dir, client):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    session_files = list(input_path.glob("*.txt"))
    if not session_files:
        log.warning("No .txt files found in %s", input_dir)
        return

    log.info("Batch: %d sessions from %s", len(session_files), input_dir)
    results = {"processed": 0, "flagged": 0, "errors": 0}

    for session_file in session_files:
        log.info("Processing: %s", session_file.name)
        try:
            raw_notes = session_file.read_text(encoding="utf-8")
            profile = process_session(raw_notes, client)
            passes, issues = quality_gate(profile)

            if not passes:
                profile["_quality_flags"] = issues
                results["flagged"] += 1
                log.warning("%s flagged: %s", session_file.name, issues)
            else:
                push_to_crm(profile)

            out_file = output_path / session_file.with_suffix(".json").name
            write_profile(profile, str(out_file))
            results["processed"] += 1

        except Exception as exc:
            log.error("Error processing %s: %s", session_file.name, exc)
            results["errors"] += 1

    log.info(
        "Batch complete -- processed: %d | flagged: %d | errors: %d",
        results["processed"], results["flagged"], results["errors"],
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not ANTHROPIC_API_KEY:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key."
        )

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    parser = argparse.ArgumentParser(
        description="EdTech Session Intelligence Pipeline -- process consultant notes into CRM-ready profiles."
    )
    parser.add_argument("--input", help="Path to a single .txt file of raw notes")
    parser.add_argument("--output", help="Path to save the output .json profile")
    parser.add_argument("--batch", help="Directory of .txt session files for bulk processing")
    parser.add_argument(
        "--output-dir", default="./profiles",
        help="Output directory for batch mode (default: ./profiles)"
    )
    args = parser.parse_args()

    if args.batch:
        run_batch(args.batch, args.output_dir, client)
    else:
        run_single(args.input, args.output, client)


if __name__ == "__main__":
    main()

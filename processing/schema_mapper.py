import json
from pathlib import Path
from classifier import classify_whatsapp_message

RAW_INPUT = Path("../data/processed/whatsapp_raw_opportunities.json")
FINAL_OUTPUT = Path("../data/processed/opportunities.json")

def infer_type(role: str | None):
    if not role:
        return None
    role_lower = role.lower()
    if "intern" in role_lower:
        return "Internship"
    return "Full-Time"


def generate_opportunity_id(company, role, raw_hash):
    base = f"{company}_{role}_{raw_hash[:6]}"
    if company and role:
        return base.lower().replace(" ", "_")
    return raw_hash[:10]


def map_raw_to_schema(raw_obj):
    raw_text = raw_obj["raw_text"]
    raw_hash = raw_obj["raw_text_hash"]

    extracted = classify_whatsapp_message(raw_text)

    opportunity = {
        "opportunity_id": generate_opportunity_id(
            extracted.get("company"),
            extracted.get("role"),
            raw_hash
        ),
        "company": extracted.get("company"),
        "role": extracted.get("role"),
        "type": infer_type(extracted.get("role")),
        "eligible_branches": [],
        "eligible_batches": extracted.get("eligible_batches"),
        "min_cgpa": extracted.get("min_cgpa"),
        "location": None,
        "deadline": extracted.get("deadline"),
        "source": raw_obj.get("source"),
        "source_url": None,
        "raw_text_hash": raw_hash
    }

    return opportunity


def main():
    with open(RAW_INPUT, encoding="utf-8") as f:
        raw_opps = json.load(f)

    final_opps = []
    for raw in raw_opps:
        mapped = map_raw_to_schema(raw)
        final_opps.append(mapped)

    FINAL_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(FINAL_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(final_opps, f, indent=2, ensure_ascii=False)

    print(f"Mapped {len(final_opps)} opportunities → {FINAL_OUTPUT}")


if __name__ == "__main__":
    main()
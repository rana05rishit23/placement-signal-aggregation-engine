import re
import json
import hashlib
from pathlib import Path


KEYWORDS = ["intern", "internship", "placement", "apply", "eligible"]

WHATSAPP_FILE = Path("data/raw/whatsapp_sample.txt")
OUTPUT_FILE = Path("data/processed/whatsapp_raw_opportunities.json")

def load_messages():
    with open(WHATSAPP_FILE, encoding="utf-8") as f:
        text = f.read()

    messages = [text.strip()]
    return messages

def is_opportunity_message(message: str) -> bool:
    msg_lower = message.lower()              # make it lowercase
    return any(keyword in msg_lower for keyword in KEYWORDS)

def normalize_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def create_raw_opportunity(text, source="WhatsApp"):
    return {
        "raw_text": text,
        "raw_text_hash": hashlib.md5(text.encode()).hexdigest(),
        "source": source
    }

def save_opportunities(opps):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(opps, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    msgs = load_messages()  # all messages
    opp_msgs = [normalize_text(m) for m in msgs if is_opportunity_message(m)]
    opps = [create_raw_opportunity(m) for m in opp_msgs]

    save_opportunities(opps)
    print(f"Loaded {len(msgs)} messages")
    print(f"Saved {len(opps)} opportunities to {OUTPUT_FILE}")
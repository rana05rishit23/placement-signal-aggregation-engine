import re
from datetime import datetime
from dateutil import parser as date_parser  # from python-dateutil

def extract_company(text: str):
    patterns = [
        r"company name[:\-]\s*([A-Za-z0-9 &]+)",
        r"Company[:\-]\s*([A-Za-z0-9 &]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return None

def extract_role(text: str):
    patterns = [
        r"role[:\-]\s*([A-Za-z0-9 /&\-]+)",
        r"position[:\-]\s*([A-Za-z0-9 /&\-]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return None
def extract_batches(text: str):
    match = re.findall(r"20\d{2}", text)
    batches = sorted(set(int(y) for y in match))
    return batches if batches else None


def extract_min_cgpa(text: str):
    match = re.search(r"CGPA\s*>=?\s*(\d+(\.\d+)?)", text, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None


def extract_deadline(text: str):
    keywords = ["apply by", "last date", "deadline"]

    lower_text = text.lower()
    for kw in keywords:
        if kw in lower_text:
            try:
                date_text = lower_text.split(kw, 1)[-1][:30]
                return date_parser.parse(date_text, fuzzy=True).date().isoformat()
            except Exception:
                pass

    return None

def classify_whatsapp_message(raw_text: str):
    return {
        "company": extract_company(raw_text),
        "role": extract_role(raw_text),
        "eligible_batches": extract_batches(raw_text),
        "min_cgpa": extract_min_cgpa(raw_text),
        "deadline": extract_deadline(raw_text),
        "source": "WhatsApp"
    }

if __name__ == "__main__":
    sample = """
    Company name: Ridecell
    Role: Backend Engineering Intern
    Batch Eligible: 2026 passouts
    CGPA >= 7.5
    Apply by 20 Jan 2026
    """

    print(classify_whatsapp_message(sample))
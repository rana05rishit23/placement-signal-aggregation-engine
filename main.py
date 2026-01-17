import json
from pathlib import Path

from processing.normalizer import normalize_company, normalize_role, normalize_branches
from processing.deduplicator import deduplicate
from ranking.ranker import rank_opportunity


STUDENT_FILE = Path("data/student_profile.json")
OPPORTUNITIES_FILE = Path("data/processed/opportunities.json")


def load_student():
    with open(STUDENT_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_opportunities():
    with open(OPPORTUNITIES_FILE, encoding="utf-8") as f:
        return json.load(f)


def normalize_opportunity(opp):
    opp = opp.copy()
    opp["company"] = normalize_company(opp.get("company"))
    opp["role"] = normalize_role(opp.get("role"))
    # eligible_branches is empty for now, but call anyway
    opp["eligible_branches"] = normalize_branches(opp.get("eligible_branches"))
    return opp


def main():
    student = load_student()
    opportunities = load_opportunities()

    # Normalize
    normalized = [normalize_opportunity(o) for o in opportunities]

    # Deduplicate
    unique_opps = deduplicate(normalized)

    # Rank
    scored = []
    for opp in unique_opps:
        score = rank_opportunity(opp, student)
        scored.append((score, opp))

    # Sort by score (high to low)
    scored.sort(reverse=True, key=lambda x: x[0])

    # Print top N
    top_n = 5
    print(f"Top {min(top_n, len(scored))} opportunities for {student['name']}:\n")
    for score, opp in scored[:top_n]:
        print(f"- {opp.get('company')} | {opp.get('role')}")
        print(f"  Batches: {opp.get('eligible_batches')}")
        print(f"  Type: {opp.get('type')}, Score: {score}")
        print(f"  Deadline: {opp.get('deadline')}")
        print()


if __name__ == "__main__":
    main()
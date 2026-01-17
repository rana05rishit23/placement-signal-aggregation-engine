def rank_opportunity(opp, student):
    score = 0

    # 1) Batch eligibility
    if opp.get("eligible_batches") and student.get("graduation_year") in opp["eligible_batches"]:
        score += 50

    # 2) CGPA condition
    min_cgpa = opp.get("min_cgpa")
    if min_cgpa is None or student.get("cgpa", 0) >= min_cgpa:
        score += 30

    # 3) Internship bonus
    if opp.get("type") == "Internship":
        score += 20

    # 4) Deadline presence
    if opp.get("deadline"):
        score += 10

    return score


if __name__ == "__main__":
    student = {
        "graduation_year": 2026,
        "cgpa": 8.0
    }
    opp = {
        "eligible_batches": [2026, 2027],
        "min_cgpa": 7.5,
        "type": "Internship",
        "deadline": "2026-01-20"
    }
    print(rank_opportunity(opp, student))  # should be 50 + 30 + 20 + 10 = 110
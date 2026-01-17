def deduplicate(opportunities):
    seen = {}
    result = []

    for opp in opportunities:
        key = (opp.get("company"), opp.get("role"))
        if key not in seen:
            seen[key] = opp
            result.append(opp)
        # If the key is already seen, we just skip it for now

    return result


if __name__ == "__main__":
    sample = [
        {"company": "Google", "role": "Sde Intern"},
        {"company": "Google", "role": "Sde Intern"},
        {"company": "Microsoft", "role": "Sde Intern"}
    ]
    print(len(deduplicate(sample)))  # should print 2
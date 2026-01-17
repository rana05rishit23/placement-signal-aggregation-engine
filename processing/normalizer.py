def normalize_company(name: str | None):
    if not name:
        return None
    # Remove the word "Role" if it got stuck in the company name
    cleaned = name.replace("Role", "")
    # Remove extra spaces and fix casing (Google -> Google, microsoft -> Microsoft)
    return cleaned.strip().title()


def normalize_role(role: str | None):
    if not role:
        return None
    # Just fix spacing + casing for now
    return role.strip().title()


def normalize_branches(branches):
    if not branches:
        return []
    mapping = {
        "CSAI": "CSE",
        "CS": "CSE",
        "CSE": "CSE",
        "IT": "IT"
    }
    return list({mapping.get(b, b) for b in branches})


if __name__ == "__main__":
    print(normalize_company("Google Role"))
    print(normalize_role("software developer intern batch"))
    print(normalize_branches(["CSAI", "CS", "IT"]))

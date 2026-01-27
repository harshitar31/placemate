def analyze_role_history(chunks):
    roles = {}

    for c in chunks:
        meta = c["metadata"]
        year = meta.get("batch_year")
        role = meta.get("role")

        if year not in roles:
            roles[year] = set()

        roles[year].add(role)

    return {
        year: sorted(list(role_set))
        for year, role_set in roles.items()
    }

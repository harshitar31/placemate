def analyze_cgpa_coverage(chunks, threshold):
    total = 0
    covered = 0

    details = []

    for c in chunks:
        meta = c["metadata"]
        text = c["text"]

        role = meta.get("role")
        year = meta.get("batch_year")

        for line in text.splitlines():
            if "Minimum CGPA" in line:
                min_cgpa = float(line.split(":")[1].strip())
                total += 1

                if threshold >= min_cgpa:
                    covered += 1
                    status = "covered"
                else:
                    status = "not covered"

                details.append({
                    "year": year,
                    "role": role,
                    "min_cgpa": min_cgpa,
                    "status": status
                })

    percentage = (covered / total * 100) if total > 0 else 0

    return {
        "threshold": threshold,
        "total_roles": total,
        "covered_roles": covered,
        "coverage_percent": round(percentage, 1),
        "details": details
    }

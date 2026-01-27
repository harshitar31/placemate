def analyze_cgpa_trend(chunks):
    data = []

    for c in chunks:
        meta = c["metadata"]
        text = c["text"]

        year = meta.get("batch_year")
        role = meta.get("role")

        for line in text.splitlines():
            if "Minimum CGPA" in line:
                cgpa = float(line.split(":")[1].strip())
                data.append({
                    "year": year,
                    "role": role,
                    "min_cgpa": cgpa
                })

    return data

def analyze_package_trend(chunks):
    data = []

    for c in chunks:
        meta = c["metadata"]
        text = c["text"]

        year = meta.get("batch_year")
        role = meta.get("role")

        ctc = None
        for line in text.splitlines():
            if "CTC" in line:
                try:
                    ctc = float(line.split(":")[1].split()[0])
                except:
                    pass

        if ctc:
            data.append({
                "year": year,
                "role": role,
                "ctc_lpa": ctc
            })

    return data

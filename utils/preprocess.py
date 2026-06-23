def parse_seq(raw):

    s = (
        str(raw)
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
        .replace('"', "")
    )

    return [
        e.strip()
        for e in s.split(",")
        if e.strip().startswith("E")
    ]
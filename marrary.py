def create(w,h):
    r = []
    for i in range(w):
        row = []
        for j in range(h):
            row.append(0)
        r.append(row)
    return r
import score as S

threshold = 1.15


def equal(a, b):
    if b==0:
        b = 0.01
    if b >= 0:
        return ((a <= b * threshold) and a >= b / threshold)
    else:
        return (a <= b / threshold and a >= b * threshold)


def greatThan(a, b):
    return (a >= (b+0.1) * threshold) if b >= 0 else (a >= (b+0.1) / threshold)


def greatOrEqualThan(a, b):
    return (equal(a, b) or greatThan(a, b))

def littleThan(a, b):
    return (a <= (b-0.1) / threshold) if b >= 0 else (a <= (b-0.1) * threshold)

def littleOrEqualThan(a, b):
    return (equal(a, b) or littleThan(a, b))

def containPoint (arrays, p):
    for i in range(len(arrays)):
        a = arrays[i]
        if (a[0] == p[0] and a[1] == p[1]):
            return True
    return False


def pointEqualfunction (a, b):
    return a[0] == b[0] if a[0] != b[0] else a[1] == b[1]


def round (score):
    neg = -1 if score < 0 else 1
    abs = abs(score)
    if (abs <= S.ONE / 2):
        return 0
    if (abs <= S.TWO / 2 and abs > S.ONE / 2):
        return neg * S.ONE
    if (abs <= S.THREE / 2 and abs > S.TWO / 2):
        return neg * S.TWO
    if (abs <= S.THREE * 1.5 and abs > S.THREE / 2):
        return neg * S.THREE
    if (abs <= S.FOUR / 2 and abs > S.THREE * 1.5):
        return neg * S.THREE*2
    if (abs <= S.FIVE / 2 and abs > S.FOUR / 2):
        return neg * S.FOUR
    return neg * S.FIVE

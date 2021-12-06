#pythran export hammingdist(str, str)
def hammingdist(a, b):
    """
    Calculates the Hamming Distance between two sequences

    Returns a value in the range of [1.0-0.0]
    """
    same, compared = 0.0, 0.0
    for i in range(0, len(a)):
        if a[i] in ('?', '-') or b[i] in ('?', '-'):
            continue
        elif a[i] == b[i]:
            same += 1.0
        compared += 1.0
    return 1.0 - (same / compared)

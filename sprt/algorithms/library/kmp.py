__alg_name__ = "KMP"
__doc__ = "Algorytm Knootha-Morisa-Pratta"


def main(*, pattern: list, text: list):
    pattern_length = len(pattern)
    text_length = len(text)

    # create lps[] that will hold the longest prefix suffix
    lps = [0] * pattern_length
    j = 0  # pattern index

    # Preprocess the pattern (calculate lps[] array)
    compute_lps_array(pattern, pattern_length, lps)

    i = 0  # text index
    results = []

    while i < text_length:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == pattern_length:
            results.append(i - j)  # Found a match, append index
            j = lps[j - 1]

        # mismatch after j matches
        elif i < text_length and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return results


def compute_lps_array(pat, M, lps):
    len = 0  # length of the previous longest prefix suffix

    lps[0]  # lps[0] is always 0
    i = 1

    # the loop calculates lps[i] for i = 1 to M-1
    while i < M:
        if pat[i] == pat[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            if len != 0:
                len = lps[len - 1]
            else:
                lps[i] = 0
                i += 1


if __name__ == "__main__":
    # Example usage:
    txt = list("ABABABDABACDABABCABAB".encode())
    pat = list("ABAB".encode())
    result = main(pattern=pat, text=txt)
    print("Pattern is found at indices:", result)

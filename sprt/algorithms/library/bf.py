__alg_name__ = "Broot-Force"
__doc__ = "Algorytm brutalnej siły/naiwny do wyszukiwania podłańcuchów znaków"


def main(*, text: list, pattern: list):
    text_length, pattern_length = len(text), len(pattern)
    results = []

    if not pattern_length or not text_length or pattern_length > text_length:
        return []

    for i in range(1 + (text_length - pattern_length)):
        for j in range(pattern_length):
            if text[i + j] != pattern[j]:
                break
        else:
            results.append(i)

    return results


if __name__ == "__main__":
    # Example usage:
    text = list("helllo worlld, hello people, hello universe".encode())
    pattern = list("ll".encode())
    result = main(text=text, pattern=pattern)
    print("Pattern is found at indices:", result)

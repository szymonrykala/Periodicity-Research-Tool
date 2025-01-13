__alg_name__ = "Boyer-Moore"
__doc__ = "Algorytm wykorzystujący tablicę przsunięć do obliczania skoku"


def main(*, text: list, pattern: list):
    pattern_length = len(pattern)
    text_length = len(text)

    if pattern_length == 0 or text_length == 0 or pattern_length > text_length:
        return []

    shift_table = generate_shift_table(pattern, pattern_length)

    i = pattern_length - 1  # text index
    results = []

    while i < len(text):
        j = 0  # pattern index

        while j < pattern_length and pattern[pattern_length - j - 1] == text[i - j]:
            j += 1

        if j == pattern_length:
            # Pattern has been found in source, return index
            results.append(i - pattern_length + 1)
            i += 1

        else:
            shift = 0

            if i + j < text_length:
                shift = shift_table.get(text[i + j], pattern_length)

            if shift == 0:
                shift = pattern_length - 1

            i += shift

    return results


def generate_shift_table(pattern, pattern_length):
    """shift table is used to determien jump in text"""
    skip_list = {}
    for i in range(0, pattern_length):
        skip_list[pattern[i]] = max(1, pattern_length - i - 1)

    return skip_list


if __name__ == "__main__":
    # Example usage:
    text = list("ABCDABCDABCD".encode())
    pattern = list("ABC".encode())

    result = main(text=text, pattern=pattern)
    print(text)
    print(pattern)
    print("Pattern is found at indices:", result)

__alg_name__ = "Karp-Rabin"
__doc__ = "Algorytm Karpa Rabina - wykorzystuje haszowanie"


def main(*, text: list, pattern: list, alphabet_size: int = 256, prime: int = 1000003):
    pattern_length = len(pattern)
    text_length = len(text)

    if pattern_length == 0 or text_length == 0 or pattern_length > text_length:
        return []

    h = pow(
        alphabet_size, pattern_length - 1, prime
    )  # Calculate d^(m-1) % q for efficient rolling hash
    results = []

    # Calculate hash value for pattern and the initial substring of text
    p = 0
    t = 0
    for i in range(pattern_length):
        p = (alphabet_size * p + pattern[i]) % prime
        t = (alphabet_size * t + text[i]) % prime

    # Iterate through the text to find all occurrences
    for i in range(text_length - pattern_length + 1):
        if p == t:
            match = True
            for j in range(pattern_length):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                results.append(i)

        # Update the rolling hash for the next substring
        if i < text_length - pattern_length:
            t = (alphabet_size * (t - text[i] * h) + text[i + pattern_length]) % prime
            if t < 0:
                t = t + prime

    return results


if __name__ == "__main__":
    # Example usage:
    text = list("ABCCDDDAEFGCDD".encode())
    pattern = list("DD".encode())
    q = 101  # A prime number
    d = 256  # Assuming ASCII characters
    result = main(pattern=pattern, text=text, prime=q, alphabet_size=d)
    print("Pattern is found at positions:", result)

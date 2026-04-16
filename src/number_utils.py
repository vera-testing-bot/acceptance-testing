_ones = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
]

_tens = [
    "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
    "eighty", "ninety",
]


def number_to_words(n):
    if n < 20:
        return _ones[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        return _tens[tens] if ones == 0 else f"{_tens[tens]} {_ones[ones]}"
    hundreds, remainder = divmod(n, 100)
    tail = f" {number_to_words(remainder)}" if remainder else ""
    return f"{_ones[hundreds]} hundred{tail}"

_ones = [
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
    'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
    'sixteen', 'seventeen', 'eighteen', 'nineteen',
]

_tens = [
    '', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy',
    'eighty', 'ninety',
]


def number_to_words(n):
    if n == 0:
        return 'zero'
    parts = []
    if n >= 100:
        parts.append(_ones[n // 100] + ' hundred')
        n %= 100
    if n >= 20:
        tens_word = _tens[n // 10]
        ones_digit = n % 10
        parts.append(tens_word + (' ' + _ones[ones_digit] if ones_digit else ''))
    elif n > 0:
        parts.append(_ones[n])
    return ' '.join(parts)

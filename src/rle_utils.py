def rle_encode(s: str) -> str:
    if not s:
        return ''
    result = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            result.append(f'{count}{s[i - 1]}')
            count = 1
    result.append(f'{count}{s[-1]}')
    return ''.join(result)


def rle_decode(s: str) -> str:
    result = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j].isdigit():
            j += 1
        count = int(s[i:j])
        result.append(s[j] * count)
        i = j + 1
    return ''.join(result)

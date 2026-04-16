def rle_encode(s):
    if not s:
        return ""
    result = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            result.append(f"{count}{s[i - 1]}")
            count = 1
    result.append(f"{count}{s[-1]}")
    return "".join(result)


def rle_decode(s):
    result = []
    i = 0
    while i < len(s):
        count_str = []
        while i < len(s) and s[i].isdigit():
            count_str.append(s[i])
            i += 1
        if i < len(s):
            result.append(s[i] * int("".join(count_str)))
            i += 1
    return "".join(result)

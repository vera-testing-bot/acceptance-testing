def bubble_sort(lst):
    result = list(lst)
    n = len(result)
    for i in range(n):
        for j in range(n - 1 - i):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
    return result

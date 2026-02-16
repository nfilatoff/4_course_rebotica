from telebot import formatting

sort_hard_dict = {
    "Сортировка Хоара": """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
""",

    "Сортировка вставками": """
def insertion(data):
    N = len(data)
    for i in range(1, N):
        for j in range(i, 0, -1):
            if data[j] < data[j - 1]:
                data[j], data[j - 1] = data[j - 1], data[j]
            else:
                break
    return data
""",

    "Сортировка выбором": """
def quicksort(dataset):
    for a in range(N - 1):
    m = dataset[a]
    p = a
    for b in range(a + 1, N):  
        if m > dataset[b]:
            m = dataset[b]
            p = b

    if p != a:  
       t = dataset[a]
       dataset[a] = dataset[p]
       dataset[p] = t
    return dataset
"""
}

sort_dict = {
    "Сортировка Хоара": "Сложность: O(n*log(n))",
    "Сортировка вставками": "Сложность: O(n^2)",
    "Сортировка выбором": "Сложность: O(n^2)"
}


def sort(name: str):
    code = formatting.hcode(sort_hard_dict[name])
    sort_info = f"{name}:\n\nКод:\n{code}\n\n{sort_dict[name]}"
    return sort_info


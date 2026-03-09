from numba import njit
import time
import random

def make_array(n):
    if n ==1:
        return [random.randint(1, 1000)]
    return make_array(n-1) + [random.randint(1, 1000)]

# def square(x):
#     return x * x
#
# def heavy(n):
#     total = 0
#     for i in range(n):
#         total += square(i)
#     return total
#
#
# if __name__ == "__main__":
#     n = 30_000_000
#
#     start = time.time()
#     result = heavy(n)
#     end = time.time()
#
#     print("Результат:", result)
#     print("Время:", round(end - start, 3), "сек")

@njit
def bingo(arr):

    max = len(arr)-1
    value = arr[max]
    for i in range(max-1,-1,-1):
        if value<arr[i]:
            value = arr[i]

    while max and arr[max]==value:
        max -= 1

    while max:
        newValue = value
        value = arr[max]

        for i in range(max-1,-1,-1):
            if arr[i]==newValue:
                arr[i],arr[max] = arr[max], arr[i]
                max-=1
            elif arr[i]>value:
                value = arr[i]
        while max and arr[max]==value:
            max-=1
    return arr

if __name__ == "__main__":
    #n = 30_000_000
    arr = make_array(400)

    start = time.time()
    result = bingo(arr)
    end = time.time()

    print("Результат:", result)
    print("Время:", round(end - start, 3), "сек")

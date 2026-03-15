import time
import random
from numba import njit

@njit
def make_array(n):
    if n ==1:
        return [random.randint(1, 1000)]
    return make_array(n-1) + [random.randint(1, 1000)]

@njit
def merge(a, b):
    i = 0
    j = 0
    res = []

    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            res.append(a[i])
            i += 1
        else:
            res.append(b[j])
            j += 1
    res += a[i:]+b[j:]
    print(res)
    return res

@njit
def fibonacci(n):
    if n in (1,2):
        return 1
    return fibonacci(n-1)+fibonacci(n-2)


# t = time.perf_counter()
# #print(fibonacci(20))
# merge(make_array(5_000), make_array(10_000))
# print(time.perf_counter()-t)

fibonacci(10)
# время для 44
t = time.perf_counter()
fibonacci(44)
t44 = time.perf_counter() - t

# время для 45
t = time.perf_counter()
fibonacci(45)
t45 = time.perf_counter() - t

print("t44 =", t44)
print("t45 =", t45)
print("Во сколько раз дольше:", t45 / t44)


#merge(a, b)
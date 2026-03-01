import time

def square(x):
    return x * x

def heavy(n):
    total = 0
    for i in range(n):
        total += square(i)
    return total


if __name__ == "__main__":
    n = 30_000_000

    start = time.time()
    result = heavy(n)
    end = time.time()

    print("Результат:", result)
    print("Время:", round(end - start, 3), "сек")
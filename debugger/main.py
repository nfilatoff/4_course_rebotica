import random

def randomer():
    return int(random.randint(1, 1000))

def start():
    counter = []
    for _ in range(100000):
        counter.append(randomer())
    return counter

def analyze():
    data = start()
    ll = len(data)
    data = [u for u in data if u % 10 == 7]
    print(len(data) / ll * 100)


if __name__ == '__main__':
    analyze()

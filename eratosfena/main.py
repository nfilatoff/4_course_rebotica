import random

def sieve(n):
    primes = [True] * (n + 1)
    primes[0:2] = [False, False]

    for p in range(2, int(n ** 0.5) + 1):
        if primes[p]:
            for i in range(p * p, n + 1, p):
                primes[i] = False

    return [i for i in range(n + 1) if primes[i]]


def bot():
    while True:
        print("\n'Решето Эратосфена'")
        print("1 — Ввести число самому")
        print("2 — Случайное число")
        print("3 — Выход")

        choice = input("Выбери режим (1, 2 или 3): ")

        if choice == "1":
            try:
                n = int(input("Введи число (>=2): "))
                if n < 2:
                    print("❌ Число должно быть >= 2")
                    continue
            except ValueError:
                print("❌ Это не число!")
                continue

        elif choice == "2":
            n = random.randint(10, 100)
            print(f"🎲 Компьютер выбрал число: {n}")

        elif choice == "3":
            print("👋 Выход из программы.")
            break

        else:
            print("❌ Неверный выбор!")
            continue

        primes = sieve(n)
        print(f"\n📌 Простые числа до {n}:")
        print(primes)
        print(f"🔢 Всего найдено: {len(primes)}")


if __name__ == "__main__":
    bot()
import random

def main():
    print("Добро пожаловать в игру 'Угадай число'!")
    print("Я загадал число от 1 до 100. Попробуй угадать!")

    secret_number = random.randint(1, 100)
    attempts = 1

    while True:
        try:
            guess = int(input("\nВведи свой вариант: "))
        except ValueError:
            print("Пожалуйста, введи целое число!")
            continue

        if guess < secret_number:
            print("Слишком мало!")
        elif guess > secret_number:
            print("Слишком много!")
        else:
            print(f"Поздравляю! Ты угадал число {secret_number} за {attempts} попыток!")
            break

        attempts += 1

    play_again = input("\nХочешь сыграть ещё раз? (да/нет): ").strip().lower()
    if play_again in ("да", "yes", "д"):
        main()
    else:
        print("Спасибо за игру! До свидания!")

if __name__ == "__main__":
    main()

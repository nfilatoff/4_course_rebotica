from loguru import logger

OBJECTS = 15

SPEEDS = {
    1: (70, 'Пешком'),
    2: (250, 'Велосипед'),
    3: (833, 'Машина'),
    4: (2000, "Поезд")
}

def main():
    try:
        meters = float(input('Введите количество метров: '))
        if meters <= 0:
            logger.error("Расстояние должно быть положительным!")
            return
    except ValueError:
        logger.error("Некорректный ввод расстояния!")
        return

    logger.info(f'Расстояние: {meters} м, объектов: {OBJECTS}')

    total_minutes = 0
    for i in range(1, OBJECTS+1):
        while True:
            try:
                choice = int(input(f'Объект {i}/{OBJECTS}. Выберите транспорт (1-пешком, 2-велосипед, 3-машина, 4-поезд): '))
                if choice in SPEEDS:
                    break
                else:
                    logger.warning(f'Неверный выбор {choice} для объекта {i}. Повторите ввод')
            except ValueError:
                logger.warning('Ввод должен быть числом! Повторите')

        speed, name = SPEEDS[choice]
        time_segment = meters/speed
        total_minutes += time_segment

        logger.info(f'Объект {i}:{name} | скорость {speed} м/мин | время на сегмент {time_segment:.2f} мин')

    hours = int(total_minutes//60)
    minutes = int(total_minutes%60)
    seconds = int((total_minutes * 60)%60)

    logger.success(f'Рассчет завершен! Общее время: {hours} часов {minutes} минут {seconds} секунд')
    print(f'\nИтого потребуется примерно: {hours} часов {minutes} минут {seconds} секунд')

if __name__ == '__main__':
    main()
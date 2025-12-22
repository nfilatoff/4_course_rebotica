import time

from loguru import logger

logger.info("Программа запущена")

# список объектов и их скоростей (м/с)
objects = {
    "Пешеход": 1.4,
    "Бегун": 3.5,
    "Велосипед": 5.5,
    "Самокат": 6.0,
    "Лошадь": 15.0,
    "Автомобиль (город)": 13.9,
    "Автомобиль (трасса)": 27.8,
    "Мотоцикл": 33.3,
    "Поезд": 22.2,
    "Скоростной поезд": 83.3,
    "Метро": 20.0,
    "Автобус": 16.7,
    "Трамвай": 13.0,
    "Самолёт": 250.0,
    "Птица": 12.0
}

logger.info(f"Загружено объектов: {len(objects)}")

time.sleep(1)
distance = float(input("Введите расстояние в метрах: "))
logger.info(f"Введено расстояние: {distance} м")

print("\nВремя в пути:\n")

for name, speed in objects.items():
    logger.info(f"Расчёт для объекта: {name}")

    time_seconds = distance / speed
    logger.info(f"Время в секундах: {time_seconds}")

    hours = int(time_seconds // 3600)
    minutes = int((time_seconds % 3600) // 60)

    logger.info(f"Результат: {hours} ч {minutes} мин")

    print(f"{name}: {hours} ч {minutes} мин")

logger.info("Программа завершена")
from loguru import logger
import time

#Все возможные варианты ротации: KB, MB, GB, 1 week, 2 second и другие сочетания

logger.add("log.log", compression="zip", rotation='2 second')
while True:
    logger.success("Мы запустились!")
    logger.debug("Для дебага")
    logger.info("Для простой инфы")
    logger.warning("Внимание! Неожиданное поведение!")
    logger.error("Ошибка! Бим Бим Бам Бам")
    logger.critical("Дантес, что ты наделал...")
    time.sleep(0.2)

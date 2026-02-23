import asyncio
import random
import time
import os
from aiogram.types import BufferedInputFile
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from loguru import logger
from io import BytesIO

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logger.add("sorting_bot.log", rotation="5 MB")



def bubble_sort(data):
    data = data.copy()
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data


def quick_sort(data):
    if len(data) <= 1:
        return data
    x = random.choice(data)
    low = [u for u in data if u < x]
    eq = [u for u in data if u == x]
    hi = [u for u in data if u > x]
    return quick_sort(low) + eq + quick_sort(hi)



class SortState(StatesGroup):
    waiting_for_numbers = State()


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def send_large_text(message: Message, text: str, filename: str):
    if len(text) < 4000:
        await message.answer(text)
    else:
        file = BufferedInputFile(text.encode(), filename=filename)
        await message.answer_document(file)

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Привет.\n\n"
        "Я сравниваю Bubble Sort и Quick Sort.\n\n"
        "Команды:\n"
        "/random — случайный список\n"
        "/sort — ввести свой список"
    )


@dp.message(Command("random"))
async def random_handler(message: Message):
    numbers = [random.randint(1, 1000) for _ in range(1000)]

    original_text = ",".join(map(str, numbers))
    await send_large_text(
        message,
        f"Созданный список:\n\n{original_text}",
        "original_list.txt"
    )

    bubble_start = time.perf_counter()
    bubble_result = bubble_sort(numbers)
    bubble_time = time.perf_counter() - bubble_start

    quick_start = time.perf_counter()
    quick_result = quick_sort(numbers)
    quick_time = time.perf_counter() - quick_start

    sorted_text = ",".join(map(str, quick_result))

    await send_large_text(
        message,
        f"Отсортированный список:\n\n{sorted_text}",
        "sorted_list.txt"
    )

    await message.answer(
        f"Bubble Sort: {bubble_time:.6f} сек\n"
        f"Quick Sort: {quick_time:.6f} сек"
    )


@dp.message(Command("sort"))
async def sort_command(message: Message, state: FSMContext):
    await state.set_state(SortState.waiting_for_numbers)
    await message.answer("Отправь числа через запятую.\nПример: 5,3,8,1,9")


@dp.message(SortState.waiting_for_numbers)
async def process_numbers(message: Message, state: FSMContext):
    try:
        raw = message.text.replace(" ", "")
        numbers = list(map(float, raw.split(",")))
        if sum(numbers) == int(sum(numbers)):
            numbers = list(map(int, numbers))

        original_text = ",".join(map(str, numbers))

        bubble_start = time.perf_counter()
        bubble_result = bubble_sort(numbers)
        bubble_time = time.perf_counter() - bubble_start

        quick_start = time.perf_counter()
        quick_result = quick_sort(numbers)
        quick_time = time.perf_counter() - quick_start

        sorted_text = ",".join(map(str, quick_result))

        await send_large_text(
            message,
            f"Твой список:\n\n{original_text}",
            "user_list.txt"
        )

        await send_large_text(
            message,
            f"Отсортированный список:\n\n{sorted_text}",
            "sorted_user_list.txt"
        )

        await message.answer(
            f"Bubble Sort: {bubble_time:.6f} сек\n"
            f"Quick Sort: {quick_time:.6f} сек"
        )

        logger.success("Пользовательский список отсортирован.")
        await state.clear()

    except Exception as e:
        logger.error(f"Ошибка обработки: {e}")
        await message.answer("Ошибка. Проверь формат чисел. Пример: 5,3,8,1")



async def main():
    logger.info("Бот запущен.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
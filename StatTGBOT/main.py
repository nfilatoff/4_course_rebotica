from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import F
import asyncio
from loguru import logger
from dotenv import load_dotenv
import os
import csv
from io import StringIO

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base, sessionmaker

logger.add('bot.log', level='INFO', rotation='1 MB', format='{time:HH:mm:ss} | {level} | {message}')

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 374330614

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID

logger.info('Загрузил токен из файла')

Base = declarative_base()
engine = create_engine('sqlite:///statopros.db')
Session = sessionmaker(bind=engine)

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    question = Column(String)
    answer = Column(String)

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    options = Column(String)

Base.metadata.create_all(engine)
db_path = os.path.abspath("statopros.db")
logger.success('База данных успешно создана. Путь: {db_path}')



class Opros(StatesGroup):
    answering = State()

class AdminAddQuestion(StatesGroup):
    waiting_for_question = State()
    waiting_for_options = State()

async def send_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    questions_ids = data["questions"]

    if index >= len(questions_ids):
        await message.answer(
            "Опрос завершён, спасибо",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.clear()
        return

    session = Session()
    q = session.get(Question, questions_ids[index])
    session.close()

    keyboard = [
        [KeyboardButton(text=opt.strip())]
        for opt in q.options.split(";")
    ]

    kb = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

    await message.answer(q.text, reply_markup=kb)
    await state.set_state(Opros.answering)

@dp.message(Command("add_question"))
async def add_question_start(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await message.answer("Отправь текст вопроса")
    await state.set_state(AdminAddQuestion.waiting_for_question)

@dp.message(AdminAddQuestion.waiting_for_question)
async def add_question_text(message: types.Message, state: FSMContext):
    await state.update_data(question_text=message.text)
    await message.answer("Теперь отправь варианты ответа через ;")
    await state.set_state(AdminAddQuestion.waiting_for_options)

@dp.message(AdminAddQuestion.waiting_for_options)
async def add_question_options(message: types.Message, state: FSMContext):
    data = await state.get_data()

    session = Session()
    q = Question(
        text=data["question_text"],
        options=message.text
    )
    session.add(q)
    session.commit()
    session.close()

    logger.info(f"Админ добавил вопрос: {data['question_text']}")
    await message.answer("Вопрос сохранён")
    await state.clear()

@dp.message(Command("start_opros"))
async def start_opros(message: types.Message, state: FSMContext):
    session = Session()
    questions = session.query(Question).all()
    session.close()

    if not questions:
        await message.answer("Опрос пока пуст")
        return

    await state.update_data(
        questions=[q.id for q in questions],
        index=0
    )

    await send_question(message, state)

@dp.message(Opros.answering)
async def save_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    question_id = data["questions"][index]

    session = Session()
    q = session.get(Question, question_id)

    question_text = q.text  # ← ВАЖНО

    ans = Answer(
        user_id=message.from_user.id,
        question=question_text,
        answer=message.text
    )
    session.add(ans)
    session.commit()
    session.close()

    logger.info(
        f"Ответ от {message.from_user.id}: {question_text} -> {message.text}"
    )

    await state.update_data(index=index + 1)
    await send_question(message, state)

@dp.message(Command("export_answers"))
async def export_answers(message: types.Message):
    if not is_admin(message.from_user.id):
        return

    session = Session()
    answers = session.query(Answer).all()
    session.close()

    if not answers:
        await message.answer("Ответов пока нет")
        return

    text = ""
    for a in answers:
        text += f"{a.user_id} | {a.question} | {a.answer}\n"

    await message.answer(text[:4000])

@dp.message(Command("export_csv"))
async def export_csv(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    session = Session()
    answers = session.query(Answer).all()
    session.close()

    if not answers:
        await message.answer("Ответов пока нет")
        return

    buffer = StringIO()
    writer = csv.writer(buffer)

    writer.writerow(["user_id", "question", "answer"])

    for a in answers:
        writer.writerow([a.user_id, a.question, a.answer])

    buffer.seek(0)

    csv_bytes = buffer.getvalue().encode("utf-8-sig")

    await message.bot.send_document(
        chat_id=message.chat.id,
        document=types.BufferedInputFile(
            csv_bytes,
            filename="answers.csv"
        )
    )

    logger.info(f"Админ {message.from_user.id} выгрузил ответы в CSV")
    await message.answer(
        "Выгрузка завершена",
        reply_markup=types.ReplyKeyboardRemove()
    )


async def main():
    logger.info("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

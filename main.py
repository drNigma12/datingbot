import os
import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ---------------- Profiles data (10 female profiles) ----------------
# Здесь три file_id для каждой анкеты: 'photo1', 'photo2', 'photo3'.
# Пока стоят заглушки FILE_ID_x_x — нужно заменить на реальные file_id.
#
# Структура: profiles = [ { "display_name": "Девушка 1", "photos": ["FILE_ID_1_1", "FILE_ID_1_2", "FILE_ID_1_3"],
#                           "age": "ххххх", "height": "ххххх", "weight": "ххххх", "hobby": "ххххх" }, ... ]
#
# Замени FILE_ID_... на реальные file_id (см. инструкции ниже)
PROFILES = [
    {
        "display_name": "Isabella",
        "photos": ["AgACAgIAAxkBAAIp62kjmq0FPuThO0moY4NE4lUDH4vSAAIZEmsbCvcYSV-2bf2jLKxPAQADAgADeQADNgQ", "AgACAgIAAxkBAAIp9Wkjm6yPZxlZRJJ00T4uWPLQLHvRAAIaEmsbCvcYSeNs4oe6HwpxAQADAgADeQADNgQ", "AgACAgIAAxkBAAIp92kjm-pX3R-iv0nwlUNlpkB3WbBkAAIbEmsbCvcYSdcHtieESmB-AQADAgADeQADNgQ"],
        "age": "21",
        "height": "177",
        "weight": "60",
        "hobby": "shopping, big foodie",
    },
    {
        "display_name": "Amelia",
        "photos": ["AgACAgIAAxkBAAIqL2kjn1zyn_8S-LDV5sHYZYGee63OAAIiEmsbCvcYSX2NP5mIcyRRAQADAgADeQADNgQ", "AgACAgIAAxkBAAIqMWkjn4Zw-PAdb1kegKuxWpzGhCdPAAIjEmsbCvcYSepo5B-hKRSOAQADAgADeQADNgQ", "AgACAgIAAxkBAAIqM2kjn7hOHgVLEgmzTE8Hig2ZXF4pAAIkEmsbCvcYSdrFlOVkUKsvAQADAgADeQADNgQ"],
        "age": "25",
        "height": "170",
        "weight": "49",
        "hobby": "dancing, traveling, walking, shopping",
    },
    {
        "display_name": "Alexandra",
        "photos": ["AgACAgIAAxkBAAIqNWkjoK7GewV6Xx1UgDHpJBu-iv9tAAImEmsbCvcYSaTvlf-xGgbgAQADAgADeQADNgQ", "AgACAgIAAxkBAAIqN2kjoO66AYlF_Myi7xGIhBfzwKmIAAInEmsbCvcYSdzc77ZEmTMCAQADAgADeQADNgQ", "AgACAgIAAxkBAAIqOWkjoRAt03KBHDkpCzJzdv6GpiDYAAIoEmsbCvcYSRgQsSPdA-wtAQADAgADeQADNgQ"],
        "age": "21",
        "height": "175",
        "weight": "48",
        "hobby": "tennis, padel",
    },
    {
        "display_name": "Sasha",
        "photos": ["AgACAgIAAxkBAAIqO2kjo-QeKF1ukGgPK1C3BUw41dKHAAIpEmsbCvcYSbPJtqK0dMhoAQADAgADeQADNgQ", "AgACAgIAAxkBAAIqPWkjpEPGM0Bcdy3eo7Rau1CUR_0jAAIqEmsbCvcYSSP-CFu0hLCmAQADAgADeQADNgQ", "AgACAgIAAxkBAAIqP2kjpGA91607651XC9bI1uf8GA2OAAIsEmsbCvcYSa3cQSE5ARTMAQADAgADeQADNgQ"],
        "age": "25",
        "height": "173",
        "weight": "52",
        "hobby": "reading, dancing, getting a second higher education",
    },
    {
        "display_name": "Polina",
        "photos": ["AgACAgIAAxkBAAIqQWkjpPvtaFfNy1NqpoeFK7n5BYj4AAIuEmsbCvcYSRZWcqyU1PL1AQADAgADeQADNgQ", "AgACAgIAAxkBAAIqQ2kjpRZOzu2_4fPzS02CnI60AAHKQQACLxJrGwr3GElUJ1_VF5uFKgEAAwIAA3kAAzYE", "AgACAgIAAxkBAAIqRWkjpTHIFB23hLDj-ODEUKZMWAhaAAIwEmsbCvcYSTQfMbcAAWXPpwEAAwIAA3kAAzYE"],
        "age": "24",
        "height": "164",
        "weight": "44",
        "hobby": "drumming, painting, tantra master",
    },
    {
        "display_name": "Девушка 6",
        "photos": ["FILE_ID_6_1", "FILE_ID_6_2", "FILE_ID_6_3"],
        "age": "ххххх",
        "height": "ххххх",
        "weight": "ххххх",
        "hobby": "ххххх",
    },
    {
        "display_name": "Девушка 7",
        "photos": ["FILE_ID_7_1", "FILE_ID_7_2", "FILE_ID_7_3"],
        "age": "ххххх",
        "height": "ххххх",
        "weight": "ххххх",
        "hobby": "ххххх",
    },
    {
        "display_name": "Девушка 8",
        "photos": ["FILE_ID_8_1", "FILE_ID_8_2", "FILE_ID_8_3"],
        "age": "ххххх",
        "height": "ххххх",
        "weight": "ххххх",
        "hobby": "ххххх",
    },
    {
        "display_name": "Девушка 9",
        "photos": ["FILE_ID_9_1", "FILE_ID_9_2", "FILE_ID_9_3"],
        "age": "ххххх",
        "height": "ххххх",
        "weight": "ххххх",
        "hobby": "ххххх",
    },
    {
        "display_name": "Девушка 10",
        "photos": ["FILE_ID_10_1", "FILE_ID_10_2", "FILE_ID_10_3"],
        "age": "ххххх",
        "height": "ххххх",
        "weight": "ххххх",
        "hobby": "ххххх",
    },
]

# Словарь для хранения позиции просмотра для каждого пользователя (in-memory)
# ключ: user_id -> текущее значение index (0..len(PROFILES)-1)
user_positions = {}


# ---------------- FSM --------------------

class ProfileStates(StatesGroup):
    waiting_name = State()
    waiting_gender = State()
    waiting_age = State()
    waiting_photo = State()

    edit_name = State()
    edit_gender = State()
    edit_age = State()
    edit_photo = State()


# ---------------- Buttons --------------------

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Редактировать анкету")],
        [KeyboardButton(text="Смотреть анкеты")]
    ],
    resize_keyboard=True
)

gender_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Мужской")],
        [KeyboardButton(text="Женский")]
    ],
    resize_keyboard=True
)

edit_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Изменить имя"),
            KeyboardButton(text="Изменить пол")
        ],
        [
            KeyboardButton(text="Изменить возраст"),
            KeyboardButton(text="Изменить фото")
        ],
        [
            KeyboardButton(text="Назад в меню")
        ]
    ],
    resize_keyboard=True
)

profile_actions_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❤️ Лайк"),
            KeyboardButton(text="⏭ Свайп")
        ],
        [
            KeyboardButton(text="⬅️ Вернуться в меню")
        ]
    ],
    resize_keyboard=True
)


# ---------------- Handlers --------------------

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! 👋\nТы в дейтинг-боте!\n\nОтправь /profile чтобы создать анкету"
    )

# --- Должно стоять ВЫШЕ любых хендлеров анкеты ---
@dp.message(F.photo & F.caption.startswith("getid:"))
async def get_file_id_from_photo(message: types.Message):
    key = message.caption.split("getid:")[1].strip()
    file_id = message.photo[-1].file_id
    await message.answer(f"ID для {key}:\n{file_id}")


@dp.message(Command("profile"))
async def profile(message: types.Message, state: FSMContext):
    await state.set_state(ProfileStates.waiting_name)
    await message.answer("Отправьте своё имя:")


# --- имя ---
@dp.message(ProfileStates.waiting_name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ProfileStates.waiting_gender)
    await message.answer("Укажите свой пол:", reply_markup=gender_kb)


# --- пол ---
@dp.message(ProfileStates.waiting_gender, F.text.in_(["Мужской", "Женский"]))
async def get_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(ProfileStates.waiting_age)
    await message.answer("Укажите свой возраст:", reply_markup=types.ReplyKeyboardRemove())


# --- возраст ---
@dp.message(ProfileStates.waiting_age)
async def get_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите возраст числом:")
        return
    await state.update_data(age=message.text)
    await state.set_state(ProfileStates.waiting_photo)
    await message.answer("Отправьте ваше фото:")


# --- фото ---
@dp.message(ProfileStates.waiting_photo, F.photo)
async def get_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)

    data = await state.get_data()

    text = (
        f"🎉 *Поздравляю, ваша анкета готова!*\n\n"
        f"Имя: {data['name']}\n"
        f"Пол: {data['gender']}\n"
        f"Возраст: {data['age']}"
    )

    await message.answer_photo(
        photo=data["photo"],
        caption=text,
        reply_markup=menu_kb
    )
    # НИЧЕГО НЕ ОЧИЩАЕМ!
    # Данные анкеты должны храниться


# ---------------- Редактирование анкеты ----------------

@dp.message(F.text == "Редактировать анкету")
async def edit_profile(message: types.Message, state: FSMContext):
    data = await state.get_data()  # правильный способ

    if not data:
        await message.answer("У вас пока нет анкеты. Нажмите /profile чтобы создать.")
        return

    text = (
        f"Ваши данные:\n\n"
        f"Имя: {data['name']}\n"
        f"Пол: {data['gender']}\n"
        f"Возраст: {data['age']}\n\n"
        "Что хотите изменить?"
    )

    await message.answer_photo(
        photo=data["photo"],
        caption=text,
        reply_markup=edit_kb
    )


# --- Изменить имя ---
@dp.message(F.text == "Изменить имя")
async def change_name(message: types.Message, state: FSMContext):
    await state.set_state(ProfileStates.edit_name)
    await message.answer("Введите новое имя:")


@dp.message(ProfileStates.edit_name)
async def save_new_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Имя обновлено!", reply_markup=menu_kb)
    await state.set_state(None)  # выходим из FSM, но не удаляем данные


# --- Изменить пол ---
@dp.message(F.text == "Изменить пол")
async def change_gender(message: types.Message, state: FSMContext):
    await state.set_state(ProfileStates.edit_gender)
    await message.answer("Выберите пол:", reply_markup=gender_kb)


@dp.message(ProfileStates.edit_gender, F.text.in_(["Мужской", "Женский"]))
async def save_new_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("Пол обновлён!", reply_markup=menu_kb)
    await state.set_state(None)


# --- Изменить возраст ---
@dp.message(F.text == "Изменить возраст")
async def change_age(message: types.Message, state: FSMContext):
    await state.set_state(ProfileStates.edit_age)
    await message.answer("Введите новый возраст:")


@dp.message(ProfileStates.edit_age)
async def save_new_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите возраст числом!")
        return
    await state.update_data(age=message.text)
    await message.answer("Возраст обновлён!", reply_markup=menu_kb)
    await state.set_state(None)


# --- Изменить фото ---
@dp.message(F.text == "Изменить фото")
async def change_photo(message: types.Message, state: FSMContext):
    await state.set_state(ProfileStates.edit_photo)
    await message.answer("Отправьте новое фото:")


@dp.message(ProfileStates.edit_photo, F.photo)
async def save_new_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer("Фото обновлено!", reply_markup=menu_kb)
    await state.set_state(None)


# --- Назад в меню ---
@dp.message(F.text == "Назад в меню")
async def back_to_menu(message: types.Message):
    await message.answer("Меню:", reply_markup=menu_kb)


# ----------------- Смотреть анкеты -----------------

@dp.message(F.text == "Смотреть анкеты")
async def watch_profiles(message: types.Message):
    user_id = message.from_user.id
    user_positions[user_id] = 0
    await send_profile_by_index(user_id, message.chat.id, 0)

async def send_profile_by_index(user_id: int, chat_id: int, index: int):
    if index < 0 or index >= len(PROFILES):
        await bot.send_message(chat_id, "У вас закончились анкеты.")
        return

    profile = PROFILES[index]
    photos = profile["photos"]

    media = []
    for i, file_id in enumerate(photos):
        caption = None
        if i == 0:
            caption = (
                f"<b>{profile['display_name']}</b>\n"
                f"Возраст: {profile['age']}\n"
                f"Рост: {profile['height']}\n"
                f"Вес: {profile['weight']}\n"
                f"Хобби: {profile['hobby']}"
            )

        media.append(InputMediaPhoto(
            media=file_id,
            caption=caption,
            parse_mode="HTML"
        ))

    await bot.send_media_group(chat_id=chat_id, media=media)

    await bot.send_message(chat_id, "Выберите действие:", reply_markup=profile_actions_kb)


# ---------------- Callbacks: Like / Next ----------------

@dp.message(F.text == "❤️ Лайк")
async def like_action(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    idx = user_positions.get(user_id, 0)

    profile = PROFILES[idx]

    await message.answer(
        f"У вас симпатия!\nНаписать: @wow_ch_mng"
    )


@dp.message(F.text == "⏭ Свайп")
async def swipe_action(message: types.Message):
    user_id = message.from_user.id
    idx = user_positions.get(user_id, 0)

    next_idx = idx + 1
    user_positions[user_id] = next_idx

    if next_idx >= len(PROFILES):
        await message.answer("Анкеты закончились.", reply_markup=menu_kb)
        return

    await send_profile_by_index(user_id, message.chat.id, next_idx)

@dp.message(F.text == "⬅️ Вернуться в меню")
async def back_to_main_menu(message: types.Message):
    await message.answer("Вы вернулись в меню:", reply_markup=menu_kb)



# ---------------- Utility: получить file_id отправив фото с подписью getid:имя ----------------
# Это НЕ обязательно, но удобно: отправь боту фото в личку с подписью "getid:girl1_1"
# и бот ответит file_id, который можно вставить в PROFILES.
@dp.message(F.photo & F.caption.startswith("getid:"))
async def get_file_id_from_photo(message: types.Message):
    caption = message.caption  # "getid:girl1_1"
    key = caption.split("getid:")[1].strip()
    file_id = message.photo[-1].file_id
    await message.answer(f"Получен file_id для {key}:\n{file_id}\n\nСкопируй и вставь в PROFILES.")
    # опционально можно сохранить в json / файл — левый оставлен для простоты.


# ---------------- Inline buttons builder ----------------
def build_profile_kb(idx: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❤️ Лайк", callback_data=f"like:{idx}"),
                InlineKeyboardButton(text="⏭ Свайп", callback_data=f"next:{idx}")
            ]
        ]
    )


# ----------------- Start bot -----------------

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

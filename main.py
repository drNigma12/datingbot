import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ============================== 25 АНКЕТ ПОЛНОСТЬЮ ==============================
PROFILES = [
    {"display_name": "Isabella", "username": "isabella_dubai", "photos": ["AgACAgIAAxkBAAIp62kjmq0FPuThO0moY4NE4lUDH4vSAAIZEmsbCvcYSV-2bf2jLKxPAQADAgADeQADNgQ","AgACAgIAAxkBAAIp9Wkjm6yPZxlZRJJ00T4uWPLQLHvRAAIaEmsbCvcYSeNs4oe6HwpxAQADAgADeQADNgQ","AgACAgIAAxkBAAIp92kjm-pX3R-iv0nwlUNlpkB3WbBkAAIbEmsbCvcYSdcHtieESmB-AQADAgADeQADNgQ"], "age": "21", "height": "177", "weight": "60", "hobby": "shopping, big foodie"},
    {"display_name": "Amelia", "username": "amelia_in_dubai", "photos": ["AgACAgIAAxkBAAIqL2kjn1zyn_8S-LDV5sHYZYGee63OAAIiEmsbCvcYSX2NP5mIcyRRAQADAgADeQADNgQ","AgACAgIAAxkBAAIqMWkjn4Zw-PAdb1kegKuxWpzGhCdPAAIjEmsbCvcYSepo5B-hKRSOAQADAgADeQADNgQ","AgACAgIAAxkBAAIqM2kjn7hOHgVLEgmzTE8Hig2ZXF4pAAIkEmsbCvcYSdrFlOVkUKsvAQADAgADeQADNgQ"], "age": "25", "height": "170", "weight": "49", "hobby": "dancing, traveling, walking, shopping"},
    {"display_name": "Alexandra", "username": "alexandra_dubai", "photos": ["AgACAgIAAxkBAAIqNWkjoK7GewV6Xx1UgDHpJBu-iv9tAAImEmsbCvcYSaTvlf-xGgbgAQADAgADeQADNgQ","AgACAgIAAxkBAAIqN2kjoO66AYlF_Myi7xGIhBfzwKmIAAInEmsbCvcYSdzc77ZEmTMCAQADAgADeQADNgQ","AgACAgIAAxkBAAIqOWkjoRAt03KBHDkpCzJzdv6GpiDYAAIoEmsbCvcYSRgQsSPdA-wtAQADAgADeQADNgQ"], "age": "21", "height": "175", "weight": "48", "hobby": "tennis, padel"},
    {"display_name": "Sasha", "username": "sasha_dxb", "photos": ["AgACAgIAAxkBAAIqO2kjo-QeKF1ukGgPK1C3BUw41dKHAAIpEmsbCvcYSbPJtqK0dMhoAQADAgADeQADNgQ","AgACAgIAAxkBAAIqPWkjpEPGM0Bcdy3eo7Rau1CUR_0jAAIqEmsbCvcYSSP-CFu0hLCmAQADAgADeQADNgQ","AgACAgIAAxkBAAIqP2kjpGA91607651XC9bI1uf8GA2OAAIsEmsbCvcYSa3cQSE5ARTMAQADAgADeQADNgQ"], "age": "25", "height": "173", "weight": "52", "hobby": "reading, dancing, getting a second higher education"},
    {"display_name": "Polina", "username": "polina_tantra", "photos": ["AgACAgIAAxkBAAIqQWkjpPvtaFfNy1NqpoeFK7n5BYj4AAIuEmsbCvcYSRZWcqyU1PL1AQADAgADeQADNgQ","AgACAgIAAxkBAAIqQ2kjpRZOzu2_4fPzS02CnI60AAHKQQACLxJrGwr3GElUJ1_VF5uFKgEAAwIAA3kAAzYE","AgACAgIAAxkBAAIqRWkjpTHIFB23hLDj-ODEUKZMWAhaAAIwEmsbCvcYSTQfMbcAAWXPpwEAAwIAA3kAAzYE"], "age": "24", "height": "164", "weight": "44", "hobby": "drumming, painting, tantra master"},
    {"display_name": "Lina", "username": "lina_pilates", "photos": ["AgACAgIAAxkBAAIr1WkxyKOf0lrM0Y1tjQLiOK2cZUWmAAJiDGsb7W6QSVxV3XjLealhAQADAgADeQADNgQ","AgACAgIAAxkBAAIr_GkxzCd3ji7CSkwYEtleq91dA2l7AAJ7DGsb7W6QSfhzTVGGRBteAQADAgADeQADNgQ","AgACAgIAAxkBAAIr_WkxzCfD4qdCY5U40nA_vStF7jyCAAJ8DGsb7W6QSeswWOsI0opbAQADAgADeQADNgQ"], "age": "23", "height": "161", "weight": "49", "hobby": "Pilates, photography"},
    {"display_name": "Yana", "username": "yana_travel", "photos": ["AgACAgIAAxkBAAIsAAFpMdZO2XJvs0nQrCAvWg3I4ViUJwAC_w9rG0RgkElRayOesOcH-gEAAwIAA3kAAzYE","AgACAgIAAxkBAAIsAmkx1k6hHpXPkZkEMnQlnk-2n3jgAAIBEGsbRGCQSYOE_LqE2GliAQADAgADeQADNgQ","AgACAgIAAxkBAAIsAWkx1k4W33y79WZnrxzG8wbBX1QKAAMQaxtEYJBJT3x2vEXrRD0BAAMCAAN4AAM2BA"], "age": "24", "height": "164", "weight": "58", "hobby": "Travel"},
    {"display_name": "Freya", "username": "freya_swim", "photos": ["AgACAgIAAxkBAAIsBmkx1oJSO2Hl_zpcv18lk9Usj6v_AAIDEGsbRGCQSSAURHTW9ZXBAQADAgADeQADNgQ","AgACAgIAAxkBAAIsCGkx1oIkxikE7PE4Qn_jP82yT6PbAAIEEGsbRGCQSY2AAt0Wtk9mAQADAgADeQADNgQ","AgACAgIAAxkBAAIsB2kx1oJJWTmtV4gWNDUuJ94_iebMAAICEGsbRGCQSfJjR_E0MQY7AQADAgADeQADNgQ"], "age": "22", "height": "177", "weight": "58", "hobby": "Swimming"},
    {"display_name": "Kaily", "username": "kaily_fit", "photos": ["AgACAgIAAxkBAAIsDmkx1qLIE7NBqIIuC7ydfoZUulZZAAIFEGsbRGCQSc5DkU3_zhsKAQADAgADeQADNgQ","AgACAgIAAxkBAAIsDGkx1qKk-QwrYAP-h87ruB7ZUzxmAAIGEGsbRGCQSaXcjXT-uAjRAQADAgADeQADNgQ","AgACAgIAAxkBAAIsDWkx1qKxwjtAPbxVqmPMIxC1UtfKAAIHEGsbRGCQScnd1Z8xdKGZAQADAgADeQADNgQ"], "age": "21", "height": "173", "weight": "53", "hobby": "Fitness"},
    {"display_name": "Mishel", "username": "mishel_sport", "photos": ["AgACAgIAAxkBAAIsEmkx1sVPUv2JagPE6pmYumwTlz3wAAIKEGsbRGCQSTKbpwGh_dBdAQADAgADeQADNgQ","AgACAgIAAxkBAAIsE2kx1sVvMGL_BVk-qRIMIsl8rpiIAAILEGsbRGCQSTwgXKJ82vYAAQEAAwIAA3kAAzYE","AgACAgIAAxkBAAIsFGkx1sXifEIROWlyUwRJSn1EY_oQAAIMEGsbRGCQSYLzAr49K_5CAQADAgADeQADNgQ"], "age": "21", "height": "177", "weight": "56", "hobby": "Sport"},
    {"display_name": "Jasmine", "username": "jasmine_beach", "photos": ["AgACAgIAAxkBAAIsGWkx1w8aOh-vMGi6wyosDEcP_wEQAAIREGsbRGCQSfn73c2e9vnCAQADAgADeQADNgQ","AgACAgIAAxkBAAIsGGkx1w9-ak32bno0gijc87fr2bibAAISEGsbRGCQSQKVrHoDn5hCAQADAgADeQADNgQ","AgACAgIAAxkBAAIsGmkx1w_ugCTSc5jwakypmMP61Y-kAAITEGsbRGCQSagS5LI8wsKiAQADAgADeQADNgQ"], "age": "25", "height": "160", "weight": "50", "hobby": "Walking on the beach, watching movies, dancing"},
    {"display_name": "Eva", "username": "eva_active", "photos": ["AgACAgIAAxkBAAIsIGkx10SXAAE-jFhYwlc-SvyEfvz5XwACFxBrG0RgkEllREoYB_K3cwEAAwIAA3kAAzYE","AgACAgIAAxkBAAIsHmkx10Srq14XUfZ6A_wIQNAx41orAAIVEGsbRGCQSQFeZQVufWH-AQADAgADeQADNgQ","AgACAgIAAxkBAAIsH2kx10RJcy2aHqOliqTuaRGm4G_-AAIWEGsbRGCQSeLb365q8cVWAQADAgADeQADNgQ"], "age": "27", "height": "162", "weight": "55", "hobby": "Sport"},
    {"display_name": "Leona", "username": "leona_dance", "photos": ["AgACAgIAAxkBAAIsJWkx12bk3_KpalGrpi7XnCuo1JEjAAIZEGsbRGCQSYyDiu0jhn1DAQADAgADeQADNgQ","AgACAgIAAxkBAAIsJmkx12YtVP9DMF1P2yfw05T7NSv_AAIbEGsbRGCQSUJCHAv2Ir2JAQADAgADeQADNgQ","AgACAgIAAxkBAAIsJGkx12aHyBLUnpzx1eadP-ql7SzLAAIaEGsbRGCQSfNMpDLVZF05AQADAgADeQADNgQ"], "age": "23", "height": "164", "weight": "50", "hobby": "Dancing"},
    {"display_name": "Amina", "username": "amina_cook", "photos": ["AgACAgIAAxkBAAIsLGkx15EPPOo6YCxBspXE-zZZbDwtAAIeEGsbRGCQST_T-K0kwheEAQADAgADeQADNgQ","AgACAgIAAxkBAAIsKmkx15G-gh35_w9Gx8Jn3PlPCLi0AAIcEGsbRGCQSbjCnYvrjAQaAQADAgADeQADNgQ","AgACAgIAAxkBAAIsK2kx15F0D3smqvCDZCZuK8VxuTN1AAIdEGsbRGCQSRNdmVNxQ6CiAQADAgADeQADNgQ"], "age": "30", "height": "157", "weight": "56", "hobby": "Reading, cooking"},
    {"display_name": "Nika", "username": "nika_yoga", "photos": ["AgACAgIAAxkBAAIsMmkx19KZV1j0cZCNMOb8KSUar15JAAIhEGsbRGCQSV-77wj3cqzyAQADAgADeQADNgQ","AgACAgIAAxkBAAIsMWkx19K4T2Ix-4l81VbrpTnX6kTYAAIfEGsbRGCQSQHXrHjhvqy-AQADAgADeQADNgQ","AgACAgIAAxkBAAIsMGkx19Iul7ejiDs5_Ty4er45_w9qAAIgEGsbRGCQSQvB0edTcHE0AQADAgADeQADNgQ"], "age": "27", "height": "175", "weight": "57", "hobby": "Yoga"},
    {"display_name": "Claire", "username": "claire_snowboard", "photos": ["AgACAgIAAxkBAAIsN2kx1_wsSfZ6GjxvskTjvdnR8no-AAIkEGsbRGCQSRld_6NXgcbAAQADAgADeQADNgQ","AgACAgIAAxkBAAIsNmkx1_xbaudgF-Bapg5VmoZKUrnNAAIjEGsbRGCQSXANO5g2JdMxAQADAgADeQADNgQ","AgACAgIAAxkBAAIsOGkx1_wpZpqTZAphy9lc09Ru1x7jAAIiEGsbRGCQSR6-eZdomSvVAQADAgADeQADNgQ"], "age": "25", "height": "161", "weight": "48", "hobby": "Snowboarding, shopping, theatre"},
    {"display_name": "Alina", "username": "alina_tarot", "photos": ["AgACAgIAAxkBAAIsPmkx2CBf83euOYJ1qSfoqNAuRXnxAAInEGsbRGCQSefqiN6ScKOgAQADAgADeQADNgQ","AgACAgIAAxkBAAIsPGkx2CBVFO1nMtCFxS69WNjV2L6uAAImEGsbRGCQSTFcGRyQrA_PAQADAgADeQADNgQ","AgACAgIAAxkBAAIsPWkx2CCUzPIXIXk4ykC7Fx8uW8KRAAIoEGsbRGCQSfcS3poAAQRF3gEAAwIAA3kAAzYE"], "age": "35", "height": "161", "weight": "50", "hobby": "Tarot cards, numerology, yoga, hot dancing"},
    {"display_name": "Sofi", "username": "sofi_artist", "photos": ["AgACAgIAAxkBAAIsQmkx2FhoCTYe5HXdIqxG_0cKLWSxAAIrEGsbRGCQSW3jzY-QF11bAQADAgADeQADNgQ","AgACAgIAAxkBAAIsQ2kx2FiLrTuZlxbYNWj9LatTJiQGAAIsEGsbRGCQSW1iFBT3rVJmAQADAgADeQADNgQ","AgACAgIAAxkBAAIsRGkx2Fjz9SsBikBpZ6BWmYR7iTCwAAItEGsbRGCQSTerpDMj-mT6AQADAgADeQADNgQ"], "age": "22", "height": "165", "weight": "50", "hobby": "I'm an artist"},
    {"display_name": "Alina", "username": "alina_swim", "photos": ["AgACAgIAAxkBAAIsSWkx2H446JNYBMSoYlGX8Zih5BwdAAIvEGsbRGCQSVMzOoMlXMhxAQADAgADeQADNgQ","AgACAgIAAxkBAAIsSGkx2H7spcCF7FK5I8LqCfwYPGI3AAIuEGsbRGCQSerfquy7jP_XAQADAgADeQADNgQ","AgACAgIAAxkBAAIsSmkx2H7SOuUeuiVzE7FpkYwWZaFDAAIwEGsbRGCQSbtIB7iBWHvHAQADAgADeQADNgQ"], "age": "21", "height": "172", "weight": "52", "hobby": "Swimming"},
    {"display_name": "Mary", "username": "mary_basket", "photos": ["AgACAgIAAxkBAAIsTmkx2KXYrhpAn0puKeIgcgi_gOLOAAIzEGsbRGCQSel9QNBuiuRaAQADAgADeQADNgQ","AgACAgIAAxkBAAIsT2kx2KVm9OnCVN0sND_uFV3aW2bKAAI0EGsbRGCQSdhJzbNecFrMAQADAgADeQADNgQ","AgACAgIAAxkBAAIsUGkx2KW7Rqy1ofQIy3S2ny6tikB0AAIyEGsbRGCQSbE3peL_dPBVAQADAgADeQADNgQ"], "age": "21", "height": "170", "weight": "55", "hobby": "Basketball, gym, stretching"},
    {"display_name": "Ariella", "username": "ariella_pilates", "photos": ["AgACAgIAAxkBAAIsVGkx2Mw95VLUx2lWARAZS47B-6dhAAI3EGsbRGCQSXZAqD83ShF7AQADAgADeQADNgQ","AgACAgIAAxkBAAIsVWkx2MyexQiBCbm7yLgihMvHZf2cAAI5EGsbRGCQSa9yFlgehBHlAQADAgADeQADNgQ","AgACAgIAAxkBAAIsVmkx2MxZwaYfQKQ3BCt2UQkcddtoAAI4EGsbRGCQSdq9d7-RC_NWAQADAgADeQADNgQ"], "age": "25", "height": "164", "weight": "57", "hobby": "Pilates, traveling, eating out"},
    {"display_name": "Sofia", "username": "sofia_sport", "photos": ["AgACAgIAAxkBAAIsWmkx2PMpEE1CJ3i3KMErPDzJquYyAAI_EGsbRGCQSc7X578hVN-jAQADAgADeQADNgQ","AgACAgIAAxkBAAIsW2kx2POxgRIi-UuETFGs2BIoK6J2AAI9EGsbRGCQSaGB5HwlU8u6AQADAgADeQADNgQ","AgACAgIAAxkBAAIsXGkx2POvsclfcWGc7assfOWH0SOHAAI-EGsbRGCQSYEMUgj2196EAQADAgADeQADNgQ"], "age": "20", "height": "162", "weight": "48", "hobby": "Sport"},
    {"display_name": "Vlada", "username": "vlada_sing", "photos": ["AgACAgIAAxkBAAIsYGkx2SjpjRvFg8ezkZlKAaUE5UDhAAJAEGsbRGCQSXuRBa6mVda6AQADAgADeQADNgQ","AgACAgIAAxkBAAIsYWkx2ShzhjgrqMX3LhA_ZYZGPh-3AAJBEGsbRGCQSe1U9HOC3P36AQADAgADeQADNgQ","AgACAgIAAxkBAAIsYmkx2SgAAac7lKmtjHByyxydSXnojwACQhBrG0RgkEk6BkV4oTP_9gEAAwIAA3kAAzYE"], "age": "25", "height": "165", "weight": "60", "hobby": "Swimming, singing"},
    {"display_name": "Stella", "username": "stella_snow", "photos": ["AgACAgIAAxkBAAIsZ2kx2UfqClybtNXZoohDUSODrFrwAAJFEGsbRGCQSa0JLEFBsORIAQADAgADeQADNgQ","AgACAgIAAxkBAAIsZmkx2UdM1GCgj54jhSMaYsZ9nlGIAAJEEGsbRGCQSTHfREIzQKqkAQADAgADeQADNgQ","AgACAgIAAxkBAAIsaGkx2UckEtFOj5WF01fBiP3219xzAAJGEGsbRGCQSX3KOXCq4HJ1AQADAgADeQADNgQ"], "age": "26", "height": "167", "weight": "55", "hobby": "Snowboarding"}
]

user_positions = {}
user_liked = {}

# ============================== FSM ==============================
class ProfileStates(StatesGroup):
    waiting_name = State()
    waiting_gender = State()
    waiting_age = State()
    waiting_photo = State()

# ============================== КРАСИВЫЕ КНОПКИ С ЭМОДЗИ ==============================
menu_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Edit Profile")],
    [KeyboardButton(text="Browse Profiles 👀")],
], resize_keyboard=True)

actions_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Like ❤️"), KeyboardButton(text="Next ➡️")],
    [KeyboardButton(text="Back to Menu ⬅️")]
], resize_keyboard=True)

continue_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Continue Browsing 👀")],
    [KeyboardButton(text="Back to Menu ⬅️")]
], resize_keyboard=True)

skip_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Skip")]], resize_keyboard=True, one_time_keyboard=True)

gender_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Male 👨🏻"), KeyboardButton(text="Female 👩🏻")],
    [KeyboardButton(text="Skip")]
], resize_keyboard=True, one_time_keyboard=True)

# ============================== ОБРАБОТЧИКИ ==============================
@dp.message(Command("start"))
async def start(m: types.Message):
    await m.answer("Hey! Welcome to the Dating Bot!\n\n/profile — create or edit your profile", reply_markup=menu_kb)

@dp.message(F.text == "Browse Profiles 👀")
async def browse(m: types.Message):
    user_positions[m.from_user.id] = 0
    user_liked[m.from_user.id] = False
    await show_profile(m.from_user.id, m.chat.id, 0)

async def show_profile(uid: int, chat_id: int, idx: int):
    if idx >= len(PROFILES):
        await bot.send_message(chat_id, "No more profiles!", reply_markup=menu_kb)
        return
    p = PROFILES[idx]
    media = [InputMediaPhoto(media=fid, caption=f"<b>{p['display_name']}</b>\nAge: {p['age']}\nHeight: {p['height']} cm\nWeight: {p['weight']} kg\nHobby: {p['hobby']}" if i == 0 else None, parse_mode="HTML")
             for i, fid in enumerate(p["photos"])]
    await bot.send_media_group(chat_id, media)
    await bot.send_message(chat_id, "Your action:", reply_markup=continue_kb if user_liked.get(uid, False) else actions_kb)

@dp.message(F.text == "Like ❤️")
async def like(m: types.Message):
    idx = user_positions.get(m.from_user.id, 0)
    girl = PROFILES[idx]
    text = f"It's a match with <a href='https://t.me/lina_mng_wch'>{girl['display_name']}</a>! Write her now ✉️" if girl.get("username") else f"It's a match with {girl['display_name']}! ✉️"
    user_liked[m.from_user.id] = True
    await m.answer(text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=continue_kb)

@dp.message(F.text.in_({"Next ➡️", "Continue Browsing 👀"}))
async def next_profile(m: types.Message):
    uid = m.from_user.id
    user_positions[uid] = user_positions.get(uid, 0) + 1
    user_liked[uid] = False
    await show_profile(uid, m.chat.id, user_positions[uid])

@dp.message(F.text == "Back to Menu ⬅️")
async def back_to_menu(m: types.Message):
    await m.answer("Main Menu", reply_markup=menu_kb)

# ============================== СОЗДАНИЕ ПРОФИЛЯ ==============================
@dp.message(F.text.in_({"Edit Profile", "/profile"}))
async def start_profile(m: types.Message, state: FSMContext):
    await state.set_state(ProfileStates.waiting_name)
    await m.answer("Enter your name:", reply_markup=skip_kb)

@dp.message(ProfileStates.waiting_name)
async def proc_name(m: types.Message, state: FSMContext):
    name = m.text if m.text != "Skip" else "—"
    await state.update_data(name=name)
    await state.set_state(ProfileStates.waiting_gender)
    await m.answer("Select your gender:", reply_markup=gender_kb)

@dp.message(ProfileStates.waiting_gender)
async def proc_gender(m: types.Message, state: FSMContext):
    if m.text == "Skip":
        gender = "—"
    elif "👨🏻" in m.text:
        gender = "Male"
    elif "👩🏻" in m.text:
        gender = "Female"
    else:
        await m.answer("Please choose one of the buttons below 👇")
        return
    await state.update_data(gender=gender)
    await state.set_state(ProfileStates.waiting_age)
    await m.answer("Your age:", reply_markup=skip_kb)

@dp.message(ProfileStates.waiting_age)
async def proc_age(m: types.Message, state: FSMContext):
    age = m.text if m.text.isdigit() or m.text == "Skip" else "—"
    await state.update_data(age=age)
    await state.set_state(ProfileStates.waiting_photo)
    await m.answer("Send your photo (or Skip):", reply_markup=skip_kb)

@dp.message(ProfileStates.waiting_photo)
async def proc_photo(m: types.Message, state: FSMContext):
    photo = m.photo[-1].file_id if m.photo else None
    data = await state.get_data()
    text = f"Your profile is ready!\n\nName: {data.get('name','—')}\nGender: {data.get('gender','—')}\nAge: {data.get('age','—')}"
    if photo:
        await m.answer_photo(photo, caption=text, reply_markup=menu_kb)
    else:
        await m.answer(text, reply_markup=menu_kb)
    await state.clear()

# ============================== ЗАПУСК ==============================
async def main():
    print("DATING BOT — FINAL VERSION WITH PERFECT EMOJI — LAUNCHED!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
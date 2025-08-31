import os
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import logging

from keyboards import keyboards
from texts import texts
from APIS.proxy import buying_proxy
from src.fsm_scripts import fsm_lists, FSMContext
from aiogram.types import FSInputFile, InputMediaPhoto

from database.requests_db import get_money, all_users_proxy
from src.handlers.deleting_messages import add, clear

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    add(user_id=message.from_user.id, msg_id=message.message_id)
    await clear(int(message.from_user.id))
    mes = await message.answer(texts.START_MESSAGE_1, reply_markup=keyboards.main)
    add(user_id=int(message.from_user.id), msg_id=mes.message_id )
    mes = await message.answer(texts.START_MESSAGE_2, reply_markup=keyboards.get_prices)
    add(user_id=int(message.from_user.id), msg_id=mes.message_id )

@router.message(or_f(F.text == texts.MAIN_BUTTON_2, Command("profile")))
async def users_proxy(message: Message):

    tg_id = message.from_user.id
    add(user_id=tg_id, msg_id=message.message_id)
    username = message.from_user.username

    money = await get_money(tg_id=tg_id, username=username)
    proxies = await all_users_proxy(tg_id=tg_id, username=username)
    
    await clear(int(message.from_user.id))
    
    mes =await message.answer(texts.PROFILE_INFO(money))
    add(user_id=int(message.from_user.id), msg_id=mes.message_id)


    
    for proxy in proxies:
        if proxy.ipv == 4:
            str_proxies = '<b>Телефон</b>\n'
        elif proxy.ipv == 3:
            str_proxies = '<b>ПК</b>\n'
        str_proxies += "<b>id прокси: </b>" + str(proxy.id_)+'\n'
        str_proxies += '<b>ip: </b>' + str(proxy.ip) + '\n'
        str_proxies += '<b>port: </b>' + str(proxy.port) + '\n'
        str_proxies += '<b>логин: </b>' + str(proxy.user_auth) + '\n'
        str_proxies += '<b>пароль: </b>' + str(proxy.password) + '\n'
        str_proxies += '<b>дата начала прокси: </b>' + str(proxy.date) + '\n'
        str_proxies += '<b>дата истечения прокси: </b>' + str(proxy.date_end) + '\n'
        str_proxies += '<b>протокол: </b>' + str(proxy.protocol) +'\n'
        mes = await message.answer(str_proxies, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f"Продлить прокси с id {proxy.id_}", callback_data='prolong_proxy '+str(proxy.id_))]]), parse_mode='HTML')
        add(user_id=int(message.from_user.id), msg_id=mes.message_id)


@router.message(F.text == texts.MAIN_BUTTON_3)
async def instruction(message: Message):
    add(user_id=message.from_user.id, msg_id=message.message_id)
    await clear(int(message.from_user.id))
    mes = await message.answer(texts.INSTRUCTION, reply_markup=keyboards.choose_instruction)
    add(user_id=int(message.from_user.id), msg_id=mes.message_id)

@router.message(F.text == texts.MAIN_BUTTON_4)
async def support(message: Message):
    add(user_id=message.from_user.id, msg_id=message.message_id)
    await clear(int(message.from_user.id))
    mes = await message.answer(texts.SUPPORT)
    add(user_id=int(message.from_user.id), msg_id=mes.message_id)

@router.message(F.text == "ПК")
async def instruction_PC(message: Message):
    add(user_id=message.from_user.id, msg_id=message.message_id)
    await clear(int(message.from_user.id))
    mes = await message.answer("Инструкция по установке прокси на ПК")
    add(user_id=int(message.from_user.id), msg_id=mes.message_id)

    # Список путей к изображениям
    image_paths = [
        "Images/PC/PC_0.jpg",
        "Images/PC/PC_1.jpg",
        "Images/PC/PC_2.jpg",
        "Images/PC/PC_3.jpg",
        "Images/PC/PC_4.jpg",
    ]

    # Проверим, что все файлы существуют
    valid_images = []
    for path in image_paths:
        if os.path.exists(path):
            valid_images.append(FSInputFile(path))
        else:
            logging.error(f"Файл не найден: {path}")
    
    # Создаём медиа-группу
    media = [InputMediaPhoto(media=img) for img in valid_images]

    # Отправляем альбом
    try:
        mes = await message.answer_media_group(media=media)#, caption="Инструкция по установке прокси на ПК")
        for msg in mes:
            add(user_id=int(message.from_user.id), msg_id=msg.message_id)
    except Exception as ex:
        logging.error(f"Не удалось отправить альбом {ex}")
    

@router.message(F.text == "Андроид")
async def instruction_ANDROID(message: Message):
    add(user_id=message.from_user.id, msg_id=message.message_id)
    await clear(int(message.from_user.id))
    mes = await message.answer("Инструкция по установке прокси на ПК")
    add(user_id=int(message.from_user.id), msg_id=mes.message_id)

    # Список путей к изображениям
    image_paths = [
        "Images/Android/Android_0.jpg",
        "Images/Android/Android_1.jpg",
        "Images/Android/Android_2.jpg",
        "Images/Android/Android_3.jpg",
    ]

    # Проверим, что все файлы существуют
    valid_images = []
    for path in image_paths:
        if os.path.exists(path):
            valid_images.append(FSInputFile(path))
        else:
            logging.error(f"Файл не найден: {path}")
    
    # Создаём медиа-группу
    media = [InputMediaPhoto(media=img) for img in valid_images]

    # Отправляем альбом
    try:
        mes = await message.answer_media_group(media=media)#, caption="Инструкция по установке прокси на Андроид")
        for msg in mes:
            add(user_id=int(message.from_user.id), msg_id=msg.message_id)
    except Exception as ex:
        logging.error(f"Не удалось отправить альбом {ex}")

@router.message(F.text == "Айфон")
async def instruction_IPHONE(message: Message):
    add(user_id=message.from_user.id, msg_id=message.message_id)
    await clear(int(message.from_user.id))
    mes = await message.answer("Инструкция по установке прокси на ПК")
    add(user_id=int(message.from_user.id), msg_id=mes.message_id)

    # Список путей к изображениям
    image_paths = [
        "Images/Iphone/Iphone_0.jpg",
        "Images/Iphone/Iphone_1.jpg",
        "Images/Iphone/Iphone_2.jpg",
        "Images/Iphone/Iphone_3.jpg",
    ]

    # Проверим, что все файлы существуют
    valid_images = []
    for path in image_paths:
        if os.path.exists(path):
            valid_images.append(FSInputFile(path))
        else:
            logging.error(f"Файл не найден: {path}")
    
    # Создаём медиа-группу
    media = [InputMediaPhoto(media=img) for img in valid_images]

    # Отправляем альбом
    try:
        mes = await message.answer_media_group(media=media)#, caption="Инструкция по установке прокси на Айфон")
        for msg in mes:
            add(user_id=int(message.from_user.id), msg_id=msg.message_id)
    except Exception as ex:
        logging.error(f"Не удалось отправить альбом {ex}")


@router.callback_query(F.data == 'get_prices')
async def applicate_prices(callback: CallbackQuery, state: FSMContext):
    await state.set_state(fsm_lists.Buy.limit_time)

    count_of_proxy = await buying_proxy.get_count_of_proxy()

    await callback.answer('Выберите устройство')
    await clear(int(callback.from_user.id))

    mes = await callback.message.answer("Для какого устройства вам нужен прокси?", reply_markup=keyboards.choose_device)
    add(user_id=callback.from_user.id, msg_id=mes.message_id)
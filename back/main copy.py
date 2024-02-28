import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import requests
import instaloader
import shutil
import random
import os
import json
import time

# https://rapidapi.com/3205/api/instagram120
# @nurbergenovv__

API_TOKEN = "5809466418:AAHsh_-JM8KqJfYfjtxXtWR9-KZuECynznQ"
XRapidAPIKey = "b33750133cmsh75074129c1eb3dep1fc99djsn29fc76c5cd9b"
admin_id = -1001980914004
relpyDownload = False

logging.basicConfig(level=logging.INFO)
insta = instaloader.Instaloader()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def send_startup_message(dp):
    await bot.send_message(admin_id, "Бот успешно запущен!")
    
ItemData = []
down_count = []
folder_path = "./stories"
users_data = []

if os.path.exists("users_data.json"):
    with open("users_data.json", "r") as json_file:
        try:
            users_data = json.load(json_file)
        except json.decoder.JSONDecodeError:
            pass


def save_users_data():
    with open("users_data.json", "w") as json_file:
        json.dump(users_data, json_file)


def user_exists(user_id):
    return any(user["user_id"] == user_id for user in users_data)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    if not user_exists(user_id):
        user_data = {
            "user_id": user_id,
            "username": message.from_user.username,
            "chat_id": message.chat.id,
            "first_name": message.from_user.first_name,
        }
        users_data.append(user_data)
        save_users_data()
    await message.reply(
        "Привет! Я бот, который скачивает посты, reel video, сторис и фото профиля в Instagram.\n"
        "Для скачивания поста, reels и сторис, отправь мне ссылку на них в Instagram.\n"
        "Для скачивания фото профиля, отправь мне имя пользователя Instagram с символом @ перед ним.\n"
        "Например:\n"
        "Для поста : https://www.instagram.com/p/ABC123/\n"
        "Для reels: https://www.instagram.com/reel/ABC123/\n"
        "Для сторис: https://www.instagram.com/stories/user/ABC123/\n"
        "Для фото профиля: @username"
    )


def get_users_data_str():
    user_data_str_list = []
    UserCount = f"Общие количество пользвателий: {len(users_data)}\n"
    user_data_str_list.append(UserCount)
    for user_data in users_data:
        user_data_str = (
            "--------------------------\n"
            f"First Name: {user_data['first_name']}\n"
            f"User ID: {user_data['user_id']}\n"
            f"Username: @{user_data['username']}\n"
            f"Chat ID: {user_data['chat_id']}\n"
            "--------------------------\n"
        )
        user_data_str_list.append(user_data_str)
    return "\n".join(user_data_str_list)


@dp.message_handler(commands=["checkusers"])
async def check_users(message: types.Message):
    if message.chat.id == admin_id:
        users_data_str = get_users_data_str()
        if users_data_str:
            await message.reply("Список всех пользователей:\n\n" + users_data_str)
        else:
            await message.reply("Список пользователей пуст.")
    else:
        await message.reply("Эта команда доступна только администратору бота.")


@dp.message_handler(commands=["admin"])
async def send_welcome(message: types.Message):
    chat_id = message.chat.id
    if chat_id == admin_id:
        await message.reply(
            f"ADMIN PANEL\n"
            "Включить отслежку скачиваний\n- /replyon\n"
            "--------------------------\n"
            "Выключить отслежку скачиваний\n- /replyoff\n"
            "--------------------------\n"
            "Cписок пользватели\n- /checkusers\n"
            "--------------------------\n"
            "Проверить статус бота\n- /status\n"
            "--------------------------\n"
        )
    else:
        await message.reply("Эта команда доступна только администратору бота.")


@dp.message_handler(commands=["status"])
async def send_welcome(message: types.Message):
    chat_id = message.chat.id
    if chat_id == admin_id:
        if relpyDownload:
            messreply = "Включено"
        else:
            messreply = "Выключено"
        await message.reply(
            f"Бот отлично работает!\n"
            "Параметры:\n"
            "--------------------------\n"
            f"Отслежка скачиваний:\n- {messreply}\n"
            "--------------------------\n"
        )


@dp.message_handler(commands=["replyon"])
async def send_welcome(message: types.Message):
    chat_id = message.chat.id
    if chat_id == admin_id:
        global relpyDownload
        relpyDownload = True
        await message.reply(f"Отслежка скачиваний успешно включено!")


@dp.message_handler(commands=["replyoff"])
async def send_welcome(message: types.Message):
    chat_id = message.chat.id
    if chat_id == admin_id:
        global relpyDownload
        relpyDownload = False
        await message.reply(f"Отслежка скачиваний успешно выключено!")


def download_file_from_url(file_url, output_folder):
    response = requests.get(file_url)
    if response.status_code == 200:
        file_name = os.path.basename(file_url).split("?")[0]
        os.makedirs(output_folder, exist_ok=True)
        file_path = os.path.join(output_folder, file_name)
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path
    else:
        return None


async def send_file(chat_id, file_path):
    if file_path.endswith(".jpg"):
        with open(file_path, "rb") as photo_file:
            await bot.send_photo(chat_id, photo_file)
    elif file_path.endswith(".mp4"):
        with open(file_path, "rb") as video_file:
            await bot.send_video(chat_id, video_file)
    if relpyDownload:
        await bot.send_message(admin_id, f"Post downloaded: {chat_id}")


async def send_video_to_user(chat_id, filename, has_video):
    filepath = f"./stories/{filename}"
    with open(filepath, "rb") as video_file:
        if has_video == "video":
            await bot.send_video(chat_id, video_file)
            if relpyDownload:
                await bot.send_message(admin_id, f"Story downloaded: {chat_id}")
            video_file.close()
            os.remove(filepath)
        else:
            await bot.send_photo(chat_id, video_file)
            if relpyDownload:
                await bot.send_message(admin_id, f"Story downloaded: {chat_id}")
            video_file.close()
            os.remove(filepath)
    print(True)
    time.sleep(1)


def download_media(url, folder_path, type, has_video):
    response = requests.get(url)
    if response.status_code == 200:
        rand = random.randint(00000, 99999)
        if has_video:
            has_video = "video"
        else:
            has_video = "photo"
        filename = "" + str(rand) + "_" + has_video + "." + type
        down_count.append(filename)
        down_count.append(has_video)
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "wb") as f:
            f.write(response.content)
            print("DONE")
        f.close()
        return file_path
    else:
        return None


# ---------------------------------------------------------

# stories
@dp.message_handler()
async def handle_text_message(message: types.Message):
    chat_id = message.chat.id
    text = message.text
    if (
        text.startswith("https://www.instagram.com/stories")
        or message.text.startswith("https://www.instagram.com/s")
        or message.text.startswith("https://instagram.com/stories")
        or message.text.startswith("https://instagram.com/s")
    ):
        await message.reply("Скачиваем...")
        await download_story_for_api(text, chat_id)
    elif message.text.startswith("@"):
        await download_profilePic(message, chat_id)
    elif message.text.startswith("https://www.instagram.com/reel/"):
        await DownloadReelVideo(message, chat_id, text)
    elif text.startswith("https://www.instagram.com/p/") or text.startswith(
        "https://www.instagram.com/post/"
    ):
        await downloadPostLink(message, chat_id, text)
    else:
        await message.reply("Ошибка")


# -----------------------------------------------------------

# download post
async def downloadPostLink(message, chat_id, text):
    await message.reply("Скачиваю...")
    try:
        url = "https://instagram120.p.rapidapi.com/api/instagram/links"

        payload = {"url": text}
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": XRapidAPIKey,
            "X-RapidAPI-Host": "instagram120.p.rapidapi.com",
        }

        response = requests.post(url, json=payload, headers=headers)

        data = response.json()

        for item in data:
            urls = item["urls"]
            for url_item in urls:
                file_url = url_item["url"]
                if url_item["name"] == "JPG":
                    file_path = download_file_from_url(file_url, "./post")
                    if file_path:
                        await send_file(chat_id, file_path)
                elif url_item["name"] == "MP4":
                    file_path = download_file_from_url(file_url, "./post")
                    if file_path:
                        await send_file(chat_id, file_path)
    except:
        await message.reply(
            "Пройзошла ошибка, пост не найден или проверте пожалуйста профиль открытый"
        )

#  download reels video
async def DownloadReelVideo(message, chat_id, text):
    try:
        await message.reply("Скачиваю...")
        url = "https://instagram120.p.rapidapi.com/api/instagram/links"
        payload = {"url": text}
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": XRapidAPIKey,
            "X-RapidAPI-Host": "instagram120.p.rapidapi.com",
        }
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        with open("instagram_reels.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        output_folder = "./reels/"
        data = data[0]["urls"][0]
        downloadLinkReel = data["url"]

        print(downloadLinkReel)
        response = requests.get(downloadLinkReel, stream=True)
        if response.status_code == 200:
            file_name = f"{chat_id}.mp4"
            os.makedirs(output_folder, exist_ok=True)
            file_path = os.path.join(output_folder, file_name)
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        with open(file_path, "rb") as video_file:
            await bot.send_video(chat_id, video_file)
            if relpyDownload:
                await bot.send_message(admin_id, f"Reels download: {chat_id}")
        video_file.close()
        os.remove(file_path)
    except:
        await message.reply(f"Произошла ошибка")

# download profile picture
async def download_profilePic(message, chat_id):
    username = message.text.split("@")[1]
    print(message.text.split("@")[1])
    try:
        profile = instaloader.Profile.from_username(insta.context, username)
        avatar_url = profile.profile_pic_url
        insta.download_profilepic(profile)
        image_files = []
        for file_name in os.listdir(username):
            if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
                image_files.append(file_name)
                break
        filepath = f"./{username}/{image_files[0]}"
        print(filepath)
        with open(filepath, "rb") as avatar_file:
            await bot.send_photo(chat_id, avatar_file)
            if relpyDownload:
                await bot.send_message(
                    admin_id, f"Profile picture Dowloaded: {chat_id}"
                )
        avatar_file.close()
        shutil.rmtree(username)
    except instaloader.exceptions.ProfileNotExistsException:
        await message.reply(
            f"Профиль с именем '{username}' не существует или профиль закрытый."
        )

# download stories
async def download_story_for_api(text, chat_id):
    url = "https://instagram120.p.rapidapi.com/api/instagram/links"
    payload = {"url": text}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": XRapidAPIKey,
        "X-RapidAPI-Host": "instagram120.p.rapidapi.com",
    }
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()["result"][0]
    storiesType = False
    if "video_versions" in data:
        downurl = data["video_versions"][0]["url"]
        storiesType = True
    else:
        downurl = data["image_versions2"]["candidates"][0]["url"]
        storiesType = False
    output_folder = "./stories"
    response = requests.get(downurl, stream=True)
    if response.status_code == 200:
        file_name = f"{chat_id}.mp4"
        os.makedirs(output_folder, exist_ok=True)
        file_path = os.path.join(output_folder, file_name)
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    print("File Downloaded")
    if str(file_path).endswith("mp4"):
        with open(file_path, "rb") as file:
            await bot.send_video(chat_id, file)
            file.close()
    else:
        with open(file_path, "rb") as file:
            await bot.send_photo(chat_id, file)
        file.close()
    os.remove(file_path)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=send_startup_message, skip_updates=True)

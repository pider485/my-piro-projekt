from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from pyrogram.types import ChatPermissions

import time
from time import sleep
import random
import os

import mss
import math
import re

import pyaudio
import audioop
import wave

from random import randint

def count_anek():
	i=0
	with open('anek.txt', 'r', encoding='utf-8') as file:
	    for line in file:  # итерация по файлу построчно
	        if line == '???\n':
	            i += 1
	return i


anek_count = count_anek()
def get_anek():
    an_list = []
    file_path = 'anek.txt'
    i = 0
    rand = randint(1, anek_count)
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:  # итерация по файлу построчно
            if line == '???\n':
                i += 1

            if i == rand and line != '???\n':
                an_list.append(line.strip())

    return "\n".join(an_list)  # собираем список в строку

def dynamic_user_filter():
    async def func(_, __, m):
        return m.from_user and m.from_user.id in id
    return filters.create(func)


app = Client("my_account")
global id
id = []
i=0

#--------------СОЗДАНИЯ ID------------#
def create_id():
    global id
    id.clear()  # очищаем список перед заполнением
    with open('id.txt', 'r') as file:
        content = file.read()
        con_sp = content.split()
        for i in range(1, len(con_sp), 2):  # сразу шагаем по ID
            id.append(int(con_sp[i]))
    print(id)
create_id()
#--------------СОЗДАНИЯ ID------------#


# команнда chek
@app.on_message(filters.command("chek", prefixes=".") & filters.me)
def type(_, msg):
	print(id)

# комманда add
@app.on_message(filters.command("add", prefixes=".") & filters.me)
def add_user(_, msg):
	try:
		username = msg.text.split(maxsplit=1)[1].strip().lstrip('@')
		us = app.get_users(username)
		if us.id not in id:
			with open('id.txt', 'a', encoding='utf-8') as file:
				file.write(f"\n{us.username} {us.id}\n")
			create_id()  # обновляем список сразу
			msg.reply(f"Добавлен: {us.username} ({us.id})")
	except Exception as e:
		msg.reply(f"Ошибка: {e}")

# комманда dell
@app.on_message(filters.command("dell", prefixes=".") & filters.me)
def type(_, msg):
	try:
		with open('id.txt', "r", encoding="utf-8") as f:
			lines = f.readlines()
		username = msg.text.split(maxsplit=1)[1].strip().lstrip('@')
		us = app.get_users(username)
		if us.id not in id :
			msg.reply('Ненайдено')
		else:
			finding = f"{us.username} {us.id}\n"
			with open('id.txt', "w", encoding="utf-8") as f:
				for line in lines:
					if finding in line:
						line = line.replace(finding, "")
					f.write(line)
				msg.reply(f"Видалено: {us.username} ({us.id})")
		create_id()
	except Exception as e:
		msg.reply(f"Ошибка: {e}")


# команда off
@app.on_message(filters.command("off", prefixes=".") & filters.me)
def type(_, msg):
    os.system("shutdown /s /t 0")

# команда res
@app.on_message(filters.command("res", prefixes=".") & filters.me)
def type(_, msg):
    os.system("shutdown /r /t 0")

# команда hib
@app.on_message(filters.command("hib", prefixes=".") & filters.me)
def type(_, msg):
    os.system("shutdown /h")

# команда scr
@app.on_message(filters.command("scr", prefixes=".") & dynamic_user_filter())
def type(_, msg):
	with mss.mss() as sct:
		monitor = sct.monitors[int((msg.text.split('.scr')[1]))]
		screenshot = sct.grab(monitor)
		mss.tools.to_png(screenshot.rgb, screenshot.size, output='templ/screen.png')
		app.send_photo(msg.chat.id, "templ/screen.png")

# calk
@app.on_message(filters.command("calk", prefixes=".") & dynamic_user_filter())
def type(_, msg):
	try:
		expression = msg.text.split(".calk ", maxsplit=1)[1]
		# Only allow safe characters and '!'
		if not all(c in "0123456789+-*/(). !f" for c in expression):
			msg.reply("Invalid characters in expression.")
			return

		# Replace 'n!' with 'math.factorial(n)'
		def factorial_replace(expr):
			return re.sub(r'(\d+)!', r'math.factorial(\1)', expr)

		safe_expr = factorial_replace(expression)
		result = eval(safe_expr, {"math": math})
		msg.reply(f"Result: {result}")
	except Exception as e:
		pass

# aud
@app.on_message(filters.command("aud", prefixes=".") & dynamic_user_filter())
def type(_, msg):
	seconds = int(msg.text.split(' ')[1])
	volume = 5
	try:
		volume = int(msg.text.split(' ')[2])
	except:
		pass
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	RECORD_SECONDS = seconds
	WAVE_OUTPUT_FILENAME = "templ/output.mp3"
	
	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					input_device_index=1,
					frames_per_buffer=CHUNK)
	
	print("* recording")
	frames = []
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		# Увеличиваем громкость (коэф. 2.0 = в 2 раза громче)
		louder = audioop.mul(data, 2, volume)  # (данные, ширина сэмпла, коэффициент)
		frames.append(louder)
	
	print("* done recording")
	stream.stop_stream()
	stream.close()
	p.terminate()
	
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
	
	app.send_voice(msg.chat.id, voice='templ/output.mp3')

#list
@app.on_message(filters.command("list", prefixes=".") & dynamic_user_filter())
def type(_, msg):
	app.send_document(msg.chat.id,'id.txt')

# комманда anek
@app.on_message(filters.command("anek", prefixes=".") & dynamic_user_filter())
def type(_, msg):
	an_list=get_anek()
	app.send_message(msg.chat.id, an_list)

#help
@app.on_message(filters.command("help", prefixes=".") & dynamic_user_filter())
def type(_, msg):
	msg.reply("""
scr (№ екрана)
calk (ваш пример)
aud (длина записи в С.) (громкость по умолчанию 5)
list просмотр вайт листа
off (викл пк)
hib (режим гибернации)
res (перезагрузка пк)
anek (випадковий анекдот)
""")

app.run()
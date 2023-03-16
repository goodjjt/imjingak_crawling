import requests
from bs4 import BeautifulSoup
import telegram
import schedule
import time
import json
import asyncio

# Telegram
async def bot_send(msg):
    telegram_token = "5128692345:AAHkO-3JZ9tZYP2hrS5UAlnYCrO0PiO09_A"
    telegram_id = "444879086"
    bot = telegram.Bot(token = telegram_token)
    await bot.sendMessage(chat_id=telegram_id, text=msg)

url_array = [
            'https://imjingakcamping.co.kr/module/reserv21/res_01_calendar.php?year=2023&month=03&day=25'
            ]
data_array = [
            '임진각평화누리캠핑장 https://imjingakcamping.co.kr/resv/res_01.html?checkdate=2023-03-25'
             ]

jsonData = None
cnt = 0

print("[" + "임직각 평화누리 예약" + "] ")

def message1():
    for index, value in enumerate(url_array):
        # BeautifulSoup
        response = requests.get(value)
        # time.sleep(3)
        cnt = 0
        message = "[" + data_array[index] + "]" + '\n'
        if response.status_code == 200:
            jsonData = response.json()
            # print(jsonData.get("result"))
            # print(jsonData.get("result").get("cv_a_01"))

            # matching = [s for s in jsonData.get("result").keys() if "ph" in s]
            # matching.extend([s for s in jsonData.get("result").keys() if "hl" in s])
            # print(matching)
            # data = jsonData.get("result").items()
            # print(data)
            print("index : ", index, "None : ", jsonData.get("result").items() is None)
            if jsonData.get("result").items() is not None:
                for key, value in jsonData.get("result").items():
                    if value == "0":
                        # 평화캠핑존
                        if key.startswith("ph"):
                            # print("평화캠핑존", " : ", key, " : ", value)
                            message = message + "평화캠핑존_" + key[-2:] + " : " + "Yes" + '\n'
                            cnt += 1
                        # 힐링캠핑존
                        if key.startswith("hl"):
                            # print("힐링캠핑존", " : ", key, " : ", value)
                            message = message + "힐링캠핑존_" + key[-2:] + " : " + "Yes" + '\n'
                            cnt += 1
                        # 누리캠핑존
                        if key.startswith("nr"):
                            # print("누리캠핑존", " : ", key, " : ", value)
                            message = message + "누리캠핑존_" + key[-2:] + " : " + "Yes" + '\n'
                            cnt += 1
                        # 에코캠핑존
                        if key.startswith("ec"):
                            # print("에코캠핑존", " : ", key, " : ", value)
                            message = message + "에코캠핑존_" + key[-2:] + " : " + "Yes" + '\n'
                            cnt += 1
                if cnt > 0:
                    asyncio.run(bot_send(message)) 
        else :
            print(response.status_code)

# step3.실행 주기 설정
schedule.every(30).seconds.do(message1)
# schedule.every(1).minutes.do(message1)

while True:
    schedule.run_pending()
    time.sleep(1)

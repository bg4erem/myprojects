"""
Задача: разработать программу, которая на основании данных сервиса https://openweathermap.org/ (требует регистрации,
достаточно бесплатного плана Free) будет выводить следующие данные для Вашего города:
1. День, с минимальной разницей "ощущаемой" и фактической температуры ночью (с указанием разницы в градусах Цельсия)
2. Максимальную продолжительностью светового дня (считать, как разницу между временем заката и рассвета) за ближайшие
5 дней (включая текущий), с указанием даты.
"""

import requests
import json
from datetime import datetime

with open("api_key.txt") as apifile:
    api_key = apifile.read()

city = 'Kaliningrad'
my_params = {
    'q': city,
    'appid': api_key.rstrip(),
    'units':'metric'
}

url = "http://api.openweathermap.org/data/2.5/forecast/daily"

response = requests.get(url, params=my_params)
j_data = response.json()  # response data in json

# сохранение респонса в json для отладки
# with open("json_data.json", "w", encoding="utf-8") as file:
#     json.dump(j_data, file, ensure_ascii=False, indent=4)

if response.ok:
    days_l = j_data.get("list")
    feelslike = {}
    daylight_h = {}
    for el in days_l:
        day_ts = int(el.get('dt'))
        day = datetime.utcfromtimestamp(day_ts).strftime('%A')
        date = datetime.utcfromtimestamp(day_ts).strftime('%d-%m-%Y')
        feelslike_diff = float(el.get('temp').get('night')) - float(el.get('feels_like').get('night'))
        feelslike[day] = feelslike_diff
        daylight_ts = int(el.get('sunset')) - int(el.get('sunrise'))
        if len(daylight_h) < 5:
            daylight_h[date] = daylight_ts

    # print(feelslike)
    print(f"1) {min(feelslike, key=lambda x: feelslike[x])} (difference: {min(feelslike.values())} °C)")
    print(f"2) Max daylight hours: {datetime.utcfromtimestamp(max(daylight_h.values())).strftime('%H:%M:%S')} "
          f"(on {max(daylight_h, key=lambda x: daylight_h[x])})")
else:
    print(f"Ответ сервера не ОК. Код ответа: {response.status_code}. "
          f"Попробуй проверить API ключ (должен быть в файле 'api_key.txt')")


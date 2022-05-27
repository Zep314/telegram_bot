# import json
# import time

# s = '{"Headline": {"EffectiveDate": "2022-05-28T19:00:00+03:00", "EffectiveEpochDate": 1653753600, "Severity": 3, "Text": "\u0421\u0443\u0431\u0431\u043e\u0442\u0430, \u0432\u0435\u0447\u0435\u0440 - \u0412\u043e\u0441\u043a\u0440\u0435\u0441\u0435\u043d\u044c\u0435, \u0443\u0442\u0440\u043e: \u043e\u0436\u0438\u0434\u0430\u0435\u0442\u0441\u044f \u0434\u043e\u0436\u0434\u043b\u0438\u0432\u0430\u044f \u043f\u043e\u0433\u043e\u0434\u0430", "Category": "rain", "EndDate": "2022-05-29T13:00:00+03:00", "EndEpochDate": 1653818400, "MobileLink": "http://www.accuweather.com/ru/ru/kirov/288509/daily-weather-forecast/288509?unit=c", "Link": "http://www.accuweather.com/ru/ru/kirov/288509/daily-weather-forecast/288509?unit=c"}, "DailyForecasts": [{"Date": "2022-05-26T07:00:00+03:00", "EpochDate": 1653537600, "Temperature": {"Minimum": {"Value": 3.7, "Unit": "C", "UnitType": 17}, "Maximum": {"Value": 11.5, "Unit": "C", "UnitType": 17}}, "Day": {"Icon": 12, "IconPhrase": "\u041b\u0438\u0432\u043d\u0438", "HasPrecipitation": true, "PrecipitationType": "Rain", "PrecipitationIntensity": "Light"}, "Night": {"Icon": 35, "IconPhrase": "\u041e\u0431\u043b\u0430\u0447\u043d\u043e \u0441 \u043f\u0440\u043e\u044f\u0441\u043d\u0435\u043d\u0438\u044f\u043c\u0438", "HasPrecipitation": false}, "Sources": ["AccuWeather"], "MobileLink": "http://www.accuweather.com/ru/ru/kirov/288509/daily-weather-forecast/288509?day=1&unit=c", "Link": "http://www.accuweather.com/ru/ru/kirov/288509/daily-weather-forecast/288509?day=1&unit=c"}]}'

# json = json.loads(s)

# #print(json)

# print(json['DailyForecasts'][0]['Date'])
# print(json['DailyForecasts'][0]['Temperature']['Minimum']['Value'])
# print(json['DailyForecasts'][0]['Temperature']['Maximum']['Value'])
# print(json['DailyForecasts'][0]['Day']['IconPhrase'])
# print(json['DailyForecasts'][0]['Day']['Icon'])
# print(json['DailyForecasts'][0]['Night']['IconPhrase'])
# print(json['DailyForecasts'][0]['Night']['Icon'])
# print(json['DailyForecasts'][0]['Link'])

s = '2022-05-26T07:00:00+03:00'

print(f'{".".join(list( reversed(s.split("T")[0].split("-")) ))} {s.split("T")[1][:5]}')

s = '0123456789'

print(s)
while len(s)>0:
    print(s[:3])
    s = s[3:]

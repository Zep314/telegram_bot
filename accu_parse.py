# Методы для обработки JSON от accuweather 

import accu_model

# Класс обработки запроса по городу
class AccuWeatherCityJsonParse:
    def __init__(self,json_string):
        self.awc = accu_model.AccuWeatherCity() # Наша модель
        self.json = json_string

    def Parse(self):                # Разбираем запрос по городу
        if len(self.json) > 0:
            self.awc.key = self.json[0]['Key']                              
            self.awc.name = self.json[0]['LocalizedName']                    
            self.awc.country = self.json[0]['Country']['LocalizedName']      
            self.awc.time_offset = self.json[0]['TimeZone']['GmtOffset']     
        return self.awc

# Класс обработки запроса по прогнозу
class AccuWeatherForecastJsonParse:
    def __init__(self,json_string):
        self.awf = accu_model.AccuWeatherForecast()
        self.json = json_string

    def Parse(self):                # Разбираем запрос по прогнозу
        if len(self.json) > 0:
            self.awf.date_time = self.json['DailyForecasts'][0]['Date']
            self.awf.temp_min = self.json['DailyForecasts'][0]['Temperature']['Minimum']['Value']
            self.awf.temp_max = self.json['DailyForecasts'][0]['Temperature']['Maximum']['Value']
            self.awf.day_predict = self.json['DailyForecasts'][0]['Day']['IconPhrase']
            self.awf.day_icon = self.json['DailyForecasts'][0]['Day']['Icon']
            self.awf.night_predict = self.json['DailyForecasts'][0]['Night']['IconPhrase']
            self.awf.night_icon = self.json['DailyForecasts'][0]['Night']['Icon']
            self.awf.link = self.json['DailyForecasts'][0]['Link']

            # Тут красиво дату-время печатаем (а то некрасивая была)
            self.awf.date_time = f'{".".join(list( reversed(self.awf.date_time.split("T")[0].split("-")) ))} '+\
                                 f'{self.awf.date_time.split("T")[1][:5]}'
        return self.awf

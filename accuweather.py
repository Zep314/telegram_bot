import requests
import json
from settings import Settings
from accu_model import AccuWeatherCity as AWC
from accu_parse import AccuWeatherCityJsonParse as AWCJP
from accu_model import AccuWeatherForecast as AWF
from accu_parse import AccuWeatherForecastJsonParse as AWFJP


class MyAccuWeather:
    def __init__(self):
        self.settings = Settings()
        self.city = AWC()
        self.forecast = AWF()
    
    def _get_city_key(self,city):
        url = self.settings.base_accuweather_url+'/locations/v1/cities/search'+\
                f'?apikey={self.settings.accuweather_tocken}&language=ru-ru'+\
                f'&q={city}'  
        response = requests.get(url)  
        data = json.loads(response.text)
        if len(data) > 0:
            self.city = AWCJP.Parse(AWCJP(data))
            return self.city
        else:
            return -1

    def GetWeather(self,city):
        city_key = self._get_city_key(city)
        if city_key == -1:
            return f'Не могу найти город *{city}*. Попробуйте еще раз.'
        else:
            url = self.settings.base_accuweather_url+f'/forecasts/v1/daily/1day/{city_key.key}'+\
                f'?apikey={self.settings.accuweather_tocken}&language=ru-ru&metric=true'
            response = requests.get(url)  

            data = json.loads(response.text)
            with open('wheather_data.json', 'w') as outfile:
                json.dump(data, outfile)
            
            if len(data) > 0:
                self.forecast = AWFJP.Parse(AWFJP(data))
                ret_str=''+\
                        f'Прогноз погоды для города *{city_key.name}*:\n'+\
                        f'\t Прогноз актуален на {self.forecast.date_time}.\n'+\
                        f'\t Сегодня температура от {self.forecast.temp_min} до {self.forecast.temp_max} градусов Цельсия.\n'+\
                        f'\t Днем ожидается {self.forecast.day_predict.lower()}, '+\
                        f' ночью - {self.forecast.night_predict.lower()}.\n'+\
                        f'\t Более подробный прогноз погоды по городу *{city_key.name}* можно посмотреть [тут]({self.forecast.link})'+\
                         ''
            else:
                ret_str = f'*Ошибка.*\n Не могу предоставить прогноз погоды по городу *{city_key.name}*. Попробуйте еще раз.'
            return ret_str

import requests
import json
from settings import Settings

class MyAccuWeather:
    def __init__(self):
        self.settings = Settings()
    
    def _get_city_key(self,city):
        url = self.settings.base_accuweather_url+'/locations/v1/cities/search'+\
                f'?apikey={self.settings.accuweather_tocken}&language=ru-ru'+\
                f'&q={city}'  
        response = requests.get(url)  
        data = json.loads(response.text)
        with open('city.json', 'w') as f:
            json.dump(data, f)
        return 288509

    def GetWeather(self,city):
        city_key = self._get_city_key(city)
        if city_key == -1:
            return f'Не могу найти город {city}. Попробуйте еще раз.'
        else:
            print(city_key)    
            url = self.settings.base_accuweather_url+f'/forecasts/v1/daily/1day/{city_key}'+\
                f'?apikey={self.settings.accuweather_tocken}&language=ru-ru&metric=true'
            response = requests.get(url)  
            data = json.loads(response.text)

            with open('weather.json', 'w') as f:
                json.dump(data, f)

            return f'Погода в городе {city_key} прекрасная!'

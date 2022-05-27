# Модель-структура данных по городу
class AccuWeatherCity:
    def __init__(self):
        self.key = 0            # Ключ города (ID)
        self.name = ''          # Наименование
        self.country = ''       # Страна
        self.time_offset = 0    # Смещение времени от UTC

# Модель - структура данных по прогнозу погоды
class AccuWeatherForecast:
    def __init__(self):         
        self.date_time = ''     # Дата-время актуальности прогноза
        self.temp_min = 0       # Минимальная температура
        self.temp_max = 0       # Максимальная температура
        self.day_predict = ''   # Предсказание погоды на день (описание)
        self.day_icon = 0       # Номер иконки на день
        self.night_predict = '' # Предсказание погоды на день (описание)
        self.night_icon = 0     # Номер иконки на ночь
        self.link = ''          # Ссылка на сайт с подробным прогнозом

        



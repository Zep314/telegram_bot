# Тут настройки бота

class Settings:
    def __init__(self):
        # Токен в telegram
        self.tocken = '5387549008:AAEbiHRs9kivi1OPqWK9CG6XewqFrIbmhVg'; # токен в телеграм

        # Токен в accuweather
        self.accuweather_tocken = '2k7ejLTq0njAmrJIa5plCwgYtENzwcII' # токен в accuweather

        # Путь к картинкам прогнозов
        self.accuweather_icon_path = 'https://developer.accuweather.com/sites/default/files'

        # URL запросов к telegram
        self.baseUrl = 'https://api.telegram.org/bot'+self.tocken+'/'

        # URL запросов к accuweather
        self.base_accuweather_url = 'http://dataservice.accuweather.com/'
        self.data_dir = 'data' # путь, где храним базу по логам пользователей
        self.life_time = 300 # после столько секунд - разрываем сессию
        
        # API котиков
        self.cats_api_url = 'https://cataas.com/cat/gif'

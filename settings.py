class Settings:
    def __init__(self):
        self.tocken = '5387549008:AAEbiHRs9kivi1OPqWK9CG6XewqFrIbmhVg'; # токен в телеграм
        self.accuweather_tocken = 'h8AS1wwc7bYYBwW6vJjY3qik4ebgjQD9' # токен в accuweather
        self.baseUrl = 'https://api.telegram.org/bot'+self.tocken+'/'
        self.base_accuweather_url = 'http://dataservice.accuweather.com/'
        self.data_dir = 'data' # путь, где храним базу по логам пользователей
        self.life_time = 300 # после столько секунд - разрываем сессию

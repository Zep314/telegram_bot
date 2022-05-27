# Запускаемый модуль

import sys

# Сотворяем бота
from bot import GrigoryTestPythonBot

if __name__ == '__main__':
    #  Настраиваем бота
    bot = GrigoryTestPythonBot()
    # Запускаем бота в работу
    bot.run_bot()

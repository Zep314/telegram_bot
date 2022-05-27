# Модуль для работы с базой данных журнала сообщений

import os
import requests
import json
import xml.etree.ElementTree as ET

from datetime import datetime
from settings import Settings

# Класс работы с базой данных журнала сообщений
class MyIO:
    def __init__(self):
        self.settings = Settings()
        if not os.path.isdir(self.settings.data_dir): # Есть ли рабочий каталог
            os.mkdir(self.settings.data_dir) # Создаем его, если его нет

    # Добавляем сообщение в базу конкретного пользователя
    def Append(self,user_id,message): 
        with open(os.path.join(self.settings.data_dir,f'{user_id}.db'),mode = 'a', encoding="utf-8") as f:
            f.write(f"{datetime.now()};{message}\n")

    # Делаем отступы в XML файле, чтобы он был красивым
    def _indent_xml(self,elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self._indent_xml(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    # Отдаем пользователю файл журнала работы в нужном fmt формате
    def SaveLog(self,user_id,message_id,chat_id,fmt):
        # Открываем журнал на чтение
        with open(os.path.join(self.settings.data_dir,f'{user_id}.db'), mode = 'r', encoding="utf-8") as f:
            if f: 
                match fmt:
                    case 'JSON':
                        my_lines = f.readlines()
                        my_list = []
                        for i in range(0,len(my_lines)):
                            items = my_lines[i].split(";")
                            # Тут готовим сам JSON
                            my_list.append({'DateTime': items[0], 'Message': items[1].replace('\n','')})
                        file_json = os.path.join(self.settings.data_dir, f'{user_id}.json') 

                        # Подготавливаем JSON файл на отправку
                        with open(file_json, mode = 'w', encoding="utf-8") as w:
                            w.write(json.dumps(my_list, indent=4))
                        # Готовим запрос
                        with open(file_json, mode = 'r', encoding="utf-8") as w:
                            post_data = {
                                'chat_id': chat_id,
                                'caption': 'Логи в JSON',
                                'reply_to_message_id': message_id
                                }
                            post_file = {'document': w}
                            requests.post(f'{self.settings.baseUrl}sendDocument', data = post_data, files = post_file)
                        # Прибираем мусор за собой    
                        if os.path.exists(file_json):
                            os.remove(file_json)
                    case 'XML':
                        my_lines = f.readlines()
                        my_list = []
                        # Тут будем собирать XML
                        root = ET.Element('data')
                        # Собираем...
                        for i in range(0,len(my_lines)):
                            items = my_lines[i].split(";")
                            line = ET.Element('line')
                            datetime1 = ET.Element('DateTime')
                            datetime1.text = items[0]
                            line.append(datetime1)

                            message1 = ET.Element('Message')
                            message1.text = items[1].replace('\n','')
                            line.append(message1)
                            root.append(line)
                        
                        # Делаем XML красивым
                        self._indent_xml(root)

                        etree = ET.ElementTree(root)
                        file_xml = os.path.join(self.settings.data_dir, f'{user_id}.xml')
                        # Пишем XML файл
                        with open(file_xml, mode = 'w', encoding="utf-8") as w:
                            etree.write(file_xml, encoding='utf-8', xml_declaration=True)
                        # Готовим запрос на отправку    
                        with open(file_xml, mode = 'r', encoding="utf-8") as w:
                            post_data = {
                                'chat_id': chat_id,
                                'caption': 'Логи в XML',
                                'reply_to_message_id': message_id
                                }
                            post_file = {'document': w}
                            requests.post(f'{self.settings.baseUrl}sendDocument', data = post_data, files = post_file)
                        # Прибираемся за собой    
                        if os.path.exists(file_xml):
                            os.remove(file_xml)
                    case _:    
                        # При TXT формате ничего подготавливать не надо, поэтому отправляем уже открытый файл
                        post_data = {
                            'chat_id': chat_id,
                            'caption': 'Текстовые логи',
                            'reply_to_message_id': message_id
                            }
                        post_file = {'document': f}
                        requests.post(f'{self.settings.baseUrl}sendDocument', data = post_data, files = post_file)
                return True
            else:
                return False

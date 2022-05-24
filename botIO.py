
import os
import requests
import json

from datetime import datetime
from settings import Settings


class MyIO:
    def __init__(self):
        self.settings = Settings()
        if not os.path.isdir(self.settings.data_dir):
            os.mkdir(self.settings.data_dir)

    def Append(self,user_id,message):
        with open(f'{self.settings.data_dir}\{user_id}.db','a') as f:
            f.write(f"{datetime.now()};{message}\n")

    def SaveLog(self,user_id,message_id,chat_id,fmt):

        with open(f'{self.settings.data_dir}\{user_id}.db','r') as f:
            if f:
                post_data = {
                    'chat_id': chat_id,
                    'caption': 'Текстовые логи',
                    'reply_to_message_id': message_id
                    }
                match fmt:
                    case 'JSON':
                        my_lines = f.readlines()
                        print(my_lines)
                        my_list = []
                        for i in range(0,len(my_lines)):
                            items = my_lines[i].split(";")
                            my_list.append({'DateTime': items[0], 'Message': items[1]})

                        print(my_list)

                        json_str = json.dumps(my_list, indent=4)
                        print(json_str)

                    case 'XML':
                        print
                    case _:    
                        post_file = {'document': f}

                #requests.post(f'{self.settings.baseUrl}sendDocument', data = post_data, files = post_file)
                return True
            else:
                return False

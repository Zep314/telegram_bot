
import os
import requests
import json
import xml.etree.ElementTree as ET

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

    def SaveLog(self,user_id,message_id,chat_id,fmt):

        with open(f'{self.settings.data_dir}\{user_id}.db','r') as f:
            if f:
                match fmt:
                    case 'JSON':
                        my_lines = f.readlines()
                        my_list = []
                        for i in range(0,len(my_lines)):
                            items = my_lines[i].split(";")
                            my_list.append({'DateTime': items[0], 'Message': items[1].replace('\n','')})

                        file_json = f'{self.settings.data_dir}\{user_id}.json' 
                        with open(file_json,'w') as w:
                            w.write(json.dumps(my_list, indent=4))
                        
                        with open(file_json,'r') as w:
                            post_data = {
                                'chat_id': chat_id,
                                'caption': 'Логи в JSON',
                                'reply_to_message_id': message_id
                                }
                            post_file = {'document': w}
                            requests.post(f'{self.settings.baseUrl}sendDocument', data = post_data, files = post_file)
                        if os.path.exists(file_json):
                            os.remove(file_json)
                    case 'XML':
                        my_lines = f.readlines()
                        my_list = []

                        root = ET.Element('data')

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
                        
                        self._indent_xml(root)

                        etree = ET.ElementTree(root)
                        file_xml = f'{self.settings.data_dir}\{user_id}.xml'
                        with open(file_xml,'w') as w:
                            etree.write(file_xml, encoding='utf-8', xml_declaration=True)
                        with open(file_xml,'r') as w:
                            post_data = {
                                'chat_id': chat_id,
                                'caption': 'Логи в XML',
                                'reply_to_message_id': message_id
                                }
                            post_file = {'document': w}
                            requests.post(f'{self.settings.baseUrl}sendDocument', data = post_data, files = post_file)
                        if os.path.exists(file_xml):
                            os.remove(file_xml)
                    case _:    
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

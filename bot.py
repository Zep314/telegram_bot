import sys
import requests
import json
from jsonparse import JsonParse
from settings import Settings
from time import sleep

class GrigoryTestPythonBot:

    incoming_msgs = []
    offset_msg = 0

    def __init__(self):
        self.settings = Settings()

    def _send_message(self,chat_id,text,reply_to_message_id = 0):
        url = f"{self.settings.baseUrl}sendMessage?chat_id={chat_id}&text={text}"
        if reply_to_message_id: url += f"&reply_to_message_id={reply_to_message_id}"
        requests.get(url)

    def _getUpdates(self):
        url = f"{self.settings.baseUrl}getUpdates?offset={self.offset_msg}"

        response = requests.get(url)
        data = json.loads(response.text)
        
        JsonParse(data)
        
        incoming_msgs = JsonParse.Parse()


        print(data['result'])

        

    def _check_events(self):
        print("222")

#        self._send_message(418068635,"Ответ123")
#        sys.exit()

    def run_bot(self):
        print("Press Ctrl+C to exit")
        while True:
            self._check_events()
            self._getUpdates()
            sleep(1)
            sys.exit()

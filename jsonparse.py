from botIO import MyIO
import message

class JsonParse:
    def __init__(self,json_string):
        self.json = json_string
    
    def Parse(self):
        ret = []
        if len(self.json['result']) > 0:
            for result in self.json['result']:
                if 'message' in result:
                    msg = message.TeleMessage()
                    msg.user_id = result['message']['from']['id']
                    msg.first_name = result['message']['from']['first_name']
                    msg.message_text = result['message']['text']
                    msg.update_id = result['update_id']
                    msg.message_id = result['message']['message_id']
                    msg.chat_id = result['message']['chat']['id']
                    #message.TeleMessage.Print(msg)
                    out = MyIO()
                    out.Append(msg.user_id,msg.message_text)
                    ret.append(msg)
        return ret

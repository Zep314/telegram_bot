class TeleMessage:
    def __init__(self):
        user_id = 0
        first_name = ''
        message_text = ''
        update_id = 0
        message_id = 0
        chat_id = 0

    def Print(self):
        print(f"[user_id = {self.user_id}; first_name = {self.first_name}; chat_id = {self.chat_id}; update_id = {self.update_id}; message_id = {self.message_id}; message_text = {self.message_text}]")

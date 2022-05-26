class TeleMessage:
    def __init__(self):
        self.user_id = 0
        self.first_name = ''
        self.message_text = ''
        self.update_id = 0
        self.message_id = 0
        self.chat_id = 0

    def Print(self):
        print(f"[user_id = {self.user_id}; first_name = {self.first_name}; chat_id = {self.chat_id}; update_id = {self.update_id}; message_id = {self.message_id}; message_text = {self.message_text}]")

from app.message import Message

class Conversation():
    title: str
    curr_message: Message
    
    def __init__(self, title: str, curr_message: Message):
        self.title = title
        self.curr_message = curr_message
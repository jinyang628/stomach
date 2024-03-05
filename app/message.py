from abc import ABC


class Message(ABC):
    prev_message: "Message"



class UserMesa
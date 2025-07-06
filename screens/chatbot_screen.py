# screens/chatbot_screen.py
from kivymd.uix.screen import MDScreen

class ChatbotScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'chatbot_screen'
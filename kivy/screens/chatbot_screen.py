# screens/chatbot_screen.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout

class TempSpinWait(MDBoxLayout):
    pass

class ChatbotScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'chatbot_screen'
# screens/name_screen.py
from kivymd.uix.screen import MDScreen

class NameInputScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'ollama_input_screen'
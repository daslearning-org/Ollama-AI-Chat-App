import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
import sys
#from datetime import datetime

# kivy & kivymd imports
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.metrics import dp, sp
from kivy.resources import resource_add_path
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel

# other public modules
from m2r2 import convert

# IMPORTANT: Set this property for keyboard behavior
Window.softinput_mode = "below_target"

# Import your screen classes
from screens.ollama_screen import OllamaInputScreen
from screens.chatbot_screen import ChatbotScreen

# import our local api & modules
from ollamaApi import get_llm_models, chat_with_llm
from myrst import MyRstDocument

## Global definitions
# Determine the base path for your application's resources
if getattr(sys, 'frozen', False):
    # Running as a PyInstaller bundle
    base_path = sys._MEIPASS
else:
    # Running in a normal Python environment
    base_path = os.path.dirname(os.path.abspath(__file__))
kv_file_path = os.path.join(base_path, 'main_layout.kv')
kv_files_dir = os.path.join(base_path, 'kv_files')
resource_add_path(kv_files_dir)

## The APP definitions
class MyApp(MDApp):
    title = "My Ollama Chatbot"
    ollama_uri = StringProperty("")
    #icon = "assets/images/favicon.png"

    def build(self):
        # Load the main KV file which will include others
        self.ollama_uri = "http://localhost:11434"
        self.selected_llm = ""
        self.messages = []
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Green"
        self.theme_cls.theme_style = "Light"
        return Builder.load_file(kv_file_path)

    # ... (rest of your methods like go_to_chatbot, go_back_to_ollama_input, send_message, update_chatbot_welcome)
    def go_to_chatbot(self, instance, ollama_uri_widget):
        ollama_uri = ollama_uri_widget.text.strip()
        if ollama_uri:
            self.ollama_uri = ollama_uri
            self.root.current = 'chatbot_screen'
            ollama_uri_widget.text = ""
        else:
            print("Please enter your name.")
            # You might want to show a SnackBar or Toast here in a real app
            self.toast("Using default Ollama URL")
            self.root.current = 'chatbot_screen'

    def go_back_to_ollama_input(self, instance):
        self.root.current = 'ollama_input_screen'

    def toast(self, text):
        from kivymd.uix.snackbar import MDSnackbar
        MDSnackbar(
            MDLabel(
                text = text,
                font_style = "Body2"
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.3,
        ).open()

    def add_bot_message(self, instance, msg_to_add, chat_label_widget):
        # Adds the Bot msg into chat history
        rst_txt = convert(msg_to_add)
        bot_msg_label = MyRstDocument(
            text = rst_txt,
            base_font_size=36,
            padding=[dp(10), dp(10)],
            background_color = self.theme_cls.bg_normal
        )
        chat_label_widget.add_widget(bot_msg_label)

    def add_usr_message(instance, msg_to_add, chat_label_widget):
        # Adds the User msg into chat history
        usr_msg_label = MDLabel(
            size_hint_y=None,
            markup=True,
            halign='right',
            valign='top',
            padding=[dp(10), dp(10)],
            font_style="Subtitle1",
            allow_selection = True,
            allow_copy = True,
            text = f"{msg_to_add}",
        )
        usr_msg_label.bind(texture_size=usr_msg_label.setter('size'))
        chat_label_widget.add_widget(usr_msg_label)

    def send_message(self, button_instance, chat_input_widget, chat_label_widget):
        user_message = chat_input_widget.text.strip()
        if user_message:
            user_message_add = f"[b][color=#2196F3]You:[/color][/b] {user_message}"
            self.messages.append(
                {
                    "role": "user",
                    "content": user_message
                }
            )
            self.add_usr_message(user_message_add, chat_label_widget)
            chat_input_widget.text = "" # blank the input
            try:
                llm_resp = chat_with_llm(url=self.ollama_uri, model=self.selected_llm, messages=self.messages[-3:]) # Sending last three messages
                if llm_resp["role"] == "assistant":
                    self.messages.append(llm_resp)
                api_msg = llm_resp["content"]
                api_msg = f"**Bot:** \n{api_msg}"
                self.add_bot_message(self, api_msg, chat_label_widget)
            except:
                err_msg_add = f"**Error:** API failed!"
                self.add_bot_message(self, err_msg_add, chat_label_widget)
        else:
            print("Please type a message.")

    def menu_callback(self, text_item, screen):
        self.selected_llm = text_item
        screen.ids.llm_menu.text = self.selected_llm

    def update_chatbot_welcome(self, screen_instance):
        screen_instance.ids.chat_history_id.background_color = self.theme_cls.bg_normal
        if self.ollama_uri:
            ollama_models = get_llm_models(self.ollama_uri)
            menu_items = [
                {
                    "text": f"{model_name}",
                    "leading_icon": "robot-happy",
                    "on_release": lambda x=f"{model_name}": self.menu_callback(x, screen_instance),
                    "font_size": sp(24)
                } for model_name in ollama_models
            ]
            self.menu = MDDropdownMenu(
                md_bg_color="#bdc6b0",
                caller=screen_instance.ids.llm_menu,
                items=[],
            )
            if len(ollama_models) >= 1:
                self.selected_llm = menu_items[0]["text"]
                screen_instance.ids.llm_menu.text = self.selected_llm
                self.menu.items = menu_items
            else:
                # pop up to be added in case of none & disable input
                print("No Ollama LLM found!")
                self.menu.items = []
                self.selected_llm = "None"
                screen_instance.ids.llm_menu.text = self.selected_llm
            #current_timestamp = datetime.now()
            #current_time = current_timestamp.strftime('%H%M%S')
            init_msg_label = MDLabel(
                size_hint_y=None,
                markup=True,
                halign='center',
                valign='top',
                padding=[dp(10), dp(10)],
                font_style="Subtitle1",
                text = f"[color=#0000FF]Init:[/color] Your Ollama URI: {self.ollama_uri}",
                #id = f"label-{current_time}"
            )
            init_msg_label.bind(texture_size=init_msg_label.setter('size'))
            screen_instance.ids.chat_history_id.add_widget(init_msg_label)
            #screen_instance.ids.chat_history_id.text = f"Your Ollama URI: {self.ollama_uri}"
        else:
            print("Ollama URI not found")
            # add some popup error

if __name__ == '__main__':
    MyApp().run()
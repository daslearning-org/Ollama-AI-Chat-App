# python core modules
import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
import sys
import re
from threading import Thread
#from datetime import datetime

# kivy & kivymd imports
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.metrics import dp, sp
from kivy.resources import resource_add_path
from kivy.core.clipboard import Clipboard
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.boxlayout import MDBoxLayout

# other public modules
from m2r2 import convert

# IMPORTANT: Set this property for keyboard behavior
Window.softinput_mode = "below_target"

# Import your screen classes
from screens.ollama_screen import OllamaInputScreen
from screens.chatbot_screen import ChatbotScreen, TempSpinWait

# import our local api & modules
from ollamaApi import get_llm_models, chat_with_llm
from myrst import MyRstDocument

## Global definitions
__version__ = "0.2.0"
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
    top_menu = ObjectProperty()
    llm_menu = ObjectProperty()
    tmp_spin = ObjectProperty(None)

    def build(self):
        # Load the main KV file which will include others
        self.ollama_uri = "http://localhost:11434"
        self.selected_llm = ""
        self.messages = []
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Green"
        self.theme_cls.theme_style = "Light"
        self.top_menu_items = {
            "Demo": {
                "icon": "youtube",
                "action": "web",
                "url": "https://youtube.com/watch?v=a-azvqDL78k",
            },
            "Documentation": {
                "icon": "file-document-check",
                "action": "web",
                "url": "https://blog.daslearning.in/llm_ai/ollama/kivy-chat.html",
            },
            "Contact Us": {
                "icon": "card-account-phone",
                "action": "web",
                "url": "https://daslearning.in/contact/",
            },
            "Check for update": {
                "icon": "github",
                "action": "update",
                "url": "",
            }
        }
        return Builder.load_file(kv_file_path)

    def on_start(self):
        menu_items = [
            {
                "text": menu_key,
                "leading_icon": self.top_menu_items[menu_key]["icon"],
                "on_release": lambda x=menu_key: self.top_menu_callback(x),
                "font_size": sp(36)
            } for menu_key in self.top_menu_items
        ]
        self.top_menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )
        self.is_llm_running = False

    def menu_bar_callback(self, button):
        self.top_menu.caller = button
        self.top_menu.open()

    def txt_dialog_closer(self, instance):
        self.txt_dialog.dismiss()

    def top_menu_callback(self, text_item):
        self.top_menu.dismiss()
        action = ""
        url = ""
        try:
            action = self.top_menu_items[text_item]["action"]
            url = self.top_menu_items[text_item]["url"]
        except Exception as e:
            print(f"Erro in menu process: {e}")
        if action == "web" and url != "":
            self.open_link(url)
        elif action == "update":
            buttons = [
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.txt_dialog_closer
                ),
                MDFlatButton(
                    text="Releases",
                    theme_text_color="Custom",
                    text_color="green",
                    on_release=self.update_checker
                ),
            ]
            self.show_text_dialog(
                "Check for update",
                f"Your version: {__version__}",
                buttons
            )

    def show_toast_msg(self, message, is_error=False):
        from kivymd.uix.snackbar import MDSnackbar
        bg_color = (0.2, 0.6, 0.2, 1) if not is_error else (0.8, 0.2, 0.2, 1)
        MDSnackbar(
            MDLabel(
                text = message,
                font_style = "Subtitle1" # change size for android
            ),
            md_bg_color=bg_color,
            y=dp(24),
            pos_hint={"center_x": 0.5},
            duration=3
        ).open()

    def show_text_dialog(self, title, text="", buttons=[]):
        self.txt_dialog = MDDialog(
            title=title,
            text=text,
            buttons=buttons
        )
        self.txt_dialog.open()

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
            self.show_toast_msg("Using default Ollama URL")
            self.root.current = 'chatbot_screen'

    def go_back_to_ollama_input(self, instance):
        self.root.current = 'ollama_input_screen'

    def add_bot_message(self, instance, msg_to_add):
        # Adds the Bot msg into chat history
        rst_txt = convert(msg_to_add)
        bot_msg_label = MyRstDocument(
            text = rst_txt,
            base_font_size=36,
            padding=[dp(10), dp(10)],
            background_color = self.theme_cls.bg_normal
        )
        self.chat_history_id.add_widget(bot_msg_label)

    def add_usr_message(self, msg_to_add):
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
        self.chat_history_id.add_widget(usr_msg_label)

    def send_message(self, button_instance, chat_input_widget):
        if self.is_llm_running:
            self.show_toast_msg("Please wait for the current response", is_error=True)
            return
        user_message = chat_input_widget.text.strip()
        if user_message:
            user_message_add = f"[b][color=#2196F3]You:[/color][/b] {user_message}"
            self.messages.append(
                {
                    "role": "user",
                    "content": user_message
                }
            )
            self.add_usr_message(user_message_add)
            chat_input_widget.text = "" # blank the input
            self.tmp_spin = TempSpinWait()
            self.chat_history_id.add_widget(self.tmp_spin)
            ollama_thread = Thread(target=chat_with_llm, args=(self.ollama_uri, self.selected_llm, self.messages[-3:], self.ollama_callback), daemon=True)
            ollama_thread.start()
            self.is_llm_running = True
        else:
            self.show_toast_msg("Please type a message!", is_error=True)

    def ollama_callback(self, llm_resp):
        if llm_resp["role"] == "assistant":
            self.messages.append(llm_resp)
        api_msg = llm_resp["content"]
        api_msg = f"**Bot:** \n{api_msg}"
        self.chat_history_id.remove_widget(self.tmp_spin)
        self.is_llm_running = False
        self.add_bot_message(self, api_msg)

    def label_copy(self, label_text):
        #print(f"DEBUG: MarkUp Text> {label_text}")
        plain_text = re.sub(r'\[/?(?:color|b|i|u|s|sub|sup|font|font_context|font_family|font_features|size|ref|anchor|text_language).*?\]', '', label_text)
        Clipboard.copy(plain_text)

    def llm_menu_callback(self, text_item, screen):
        self.llm_menu.dismiss()
        self.selected_llm = text_item
        screen.ids.llm_menu.text = self.selected_llm

    def update_chatbot_welcome(self, screen_instance):
        screen_instance.ids.chat_history_id.background_color = self.theme_cls.bg_normal
        self.chat_history_id = screen_instance.ids.chat_history_id
        if self.ollama_uri:
            ollama_models = get_llm_models(self.ollama_uri)
            menu_items = [
                {
                    "text": f"{model_name}",
                    "leading_icon": "robot-happy",
                    "on_release": lambda x=f"{model_name}": self.llm_menu_callback(x, screen_instance),
                    "font_size": sp(24)
                } for model_name in ollama_models
            ]
            self.llm_menu = MDDropdownMenu(
                md_bg_color="#bdc6b0",
                caller=screen_instance.ids.llm_menu,
                items=[],
            )
            if len(ollama_models) >= 1:
                self.selected_llm = menu_items[0]["text"]
                screen_instance.ids.llm_menu.text = self.selected_llm
                self.llm_menu.items = menu_items
            else:
                # pop up to be added in case of none & disable input
                print("No Ollama LLM found!")
                self.llm_menu.items = []
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

    def update_checker(self, instance):
        self.txt_dialog.dismiss()
        self.open_link("https://github.com/daslearning-org/Ollama-AI-Chat-App/releases")

    def open_link(self, url):
        import webbrowser
        webbrowser.open(url)

if __name__ == '__main__':
    MyApp().run()
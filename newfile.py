
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.clipboard import Clipboard

FILE_PATH = "secret_notes.txt"

class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.foreground_color = (0, 0, 0, 1)  # စာလုံးအရောင် အမည်း
        self.background_color = (0.95, 0.95, 0.95, 1)  # အနောက်ခံ အဖြူရောင်

class CipherVaultApp(App):
    def build(self):
        self.notes_dict = {}
        
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Header
        header = Label(
            text="CipherVault Pro", 
            font_size='22sp', 
            bold=True, 
            size_hint_y=None, 
            height=40,
            color=(0.8, 0.65, 0.97, 1)
        )
        main_layout.add_widget(header)
        
        # Title Input
        main_layout.add_widget(Label(text="Note Title:", size_hint_y=None, height=25, halign='left'))
        self.title_input = CustomTextInput(multiline=False, size_hint_y=None, height=40)
        main_layout.add_widget(self.title_input)
        
        # Content Input
        main_layout.add_widget(Label(text="Secret Content / Password:", size_hint_y=None, height=25))
        self.content_input = CustomTextInput(multiline=True, size_hint_y=None, height=100)
        main_layout.add_widget(self.content_input)
        
        # Save Button
        save_btn = Button(
            text="SAVE NOTE", 
            size_hint_y=None, 
            height=45, 
            background_color=(0.2, 0.7, 0.3, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        save_btn.bind(on_press=self.save_note)
        main_layout.add_widget(save_btn)
        
        # Saved Notes List Area
        main_layout.add_widget(Label(text="Saved Notes (Click to Copy):", size_hint_y=None, height=25))
        
        self.scroll = ScrollView(size_hint=(1, 1))
        self.list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        self.scroll.add_widget(self.list_layout)
        main_layout.add_widget(self.scroll)
        
        self.load_notes()
        return main_layout

    def save_note(self, instance):
        title = self.title_input.text.strip()
        content = self.content_input.text.strip()
        
        if title and content:
            with open(FILE_PATH, "a", encoding="utf-8") as f:
                f.write(f"=== {title} ===\n{content}\n---------------------\n")
            
            self.title_input.text = ""
            self.content_input.text = ""
            self.load_notes()

    def load_notes(self):
        self.list_layout.clear_widgets()
        self.notes_dict.clear()
        
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                content = f.read()
                blocks = content.split("---------------------\n")
                for block in blocks:
                    if block.strip():
                        lines = block.strip().split("\n")
                        if lines[0].startswith("==="):
                            title = lines[0].replace("===", "").strip()
                            body = "\n".join(lines[1:])
                            self.notes_dict[title] = body
                            
                            btn = Button(
                                text=title, 
                                size_hint_y=None, 
                                height=40,
                                background_color=(0.25, 0.25, 0.35, 1)
                            )
                            btn.bind(on_press=lambda b, t=title: self.copy_note(t))
                            self.list_layout.add_widget(btn)

    def copy_note(self, title):
        if title in self.notes_dict:
            body = self.notes_dict[title]
            self.content_input.text = body
            Clipboard.copy(body)

if __name__ == "__main__":
    CipherVaultApp().run()

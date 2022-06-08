import os
from pathlib import Path

from kivy import platform
from kivy.config import Config

if platform == 'android':
    Config.set("graphics", "width", "630")
    Config.set("graphics", "height", "950")
else:
    Config.set("graphics", "width", "1200")
    Config.set("graphics", "height", "860")

from kivymd.app import MDApp

from View.Managers.manager_screen import ManagerScreen


os.environ['CURRENCY_CONVERTER_ROOT'] = str(Path(__file__).parent)


class ConverterApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'DeepOrange'
        self.manager_screen = ManagerScreen()

    def __str__(self):
        return 'Converter App'

    def build(self):
        self.manager_screen.add_widget(self.manager_screen.create_screen('main'))
        return self.manager_screen

    def get_first(self):
        self.manager_screen.switch_screen('first')


if __name__ == '__main__':
    ConverterApp().run()

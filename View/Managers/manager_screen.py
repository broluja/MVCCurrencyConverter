import os

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, WipeTransition
from kivy.clock import Clock

from View.screens import screens


class ManagerScreen(ScreenManager):
    _screens = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.transition = WipeTransition()

    def create_screen(self, name_screen):
        if name_screen not in self._screens:
            self._screens.append(name_screen)
            exec(f"import View.{screens[name_screen]}")
            self.app.load_all_kv_files(
                os.path.join(self.app.directory, "View", screens[name_screen].split(".")[0])
            )
            view = eval(
                f'View.{screens[name_screen]}.{screens[name_screen].split(".")[0]}View()'
            )
            view.name = name_screen
            return view

    def switch_screen(self, screen_name: str) -> None:
        def switch_screen(*args):
            if screen_name not in self._screens:
                screen = self.create_screen(screen_name)
                self.add_screen(screen)
            self.current = screen_name

        if screen_name not in self._screens:
            Clock.schedule_once(switch_screen)
        else:
            self.current = screen_name

    def add_screen(self, screen):
        self.add_widget(screen)

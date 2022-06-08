from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.recycleview import RecycleView
from kivymd.uix.screen import MDScreen

from View.Managers.currency_manager import CurrencyManager


class RV(RecycleView):
    error = StringProperty()

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
        CurrencyManager().get_currencies(self.on_server_data, self.on_server_failure)

    def on_server_data(self, data):
        self.data = data

    def on_server_failure(self, error):
        self.data.append({'text': error})


class SecondScreenView(MDScreen):
    recycleView = ObjectProperty(None)

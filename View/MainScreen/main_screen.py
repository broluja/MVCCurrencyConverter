from kivy.properties import NumericProperty, StringProperty
from kivymd.uix.screen import MDScreen

from View.Managers.currency_manager import CurrencyManager


class MainScreenView(MDScreen):
    flip_state = NumericProperty(0)
    rate = NumericProperty()
    error = StringProperty('Error')

    def __init__(self, **kwargs):
        super(MainScreenView, self).__init__(**kwargs)
        self.get_exchange_rate('EUR', 'RSD')

    def get_exchange_rate(self, from_currency, to_currency):
        CurrencyManager().get_exchange_rate(from_currency, to_currency, self.on_rate_success, self.on_rate_failure)

    def on_rate_success(self, rate):
        self.rate = rate

    def on_rate_failure(self, error):
        self.rate = 0
        self.error = error

    def switch_currencies(self):
        if self.flip_state == 0:
            self.flip_state = 1
            self.ids.currency_label.text = 'RSD to [color=#e87b27]EUR[/color]'
            self.get_exchange_rate('RSD', 'EUR')
            self.ids.result_label.text = ''
            self.ids.input.text = ''
        else:
            self.flip_state = 0
            self.ids.currency_label.text = 'EUR to [color=#e87b27]RSD[/color]'
            self.get_exchange_rate('EUR', 'RSD')
            self.ids.result_label.text = ''
            self.ids.input.text = ''

    def convert(self):
        if self.flip_state == 0:
            try:
                customer_input = float(self.ids.input.text)
            except ValueError:
                self.ids.result_label.text = f'Please enter valid amount'
                return
            one_eur = self.rate
            if self.rate == 0:
                self.ids.result_label.theme_text_color = 'Error'
                self.ids.result_label.text = self.error
                return
            amount = round(customer_input * one_eur, 2)
            self.ids.result_label.text = f'{self.ids.input.text} EUR is: [color=#e87b27]{amount} RSD[/color]'

        else:
            try:
                customer_input = float(self.ids.input.text)
            except ValueError:
                self.ids.result_label.text = f'Please enter valid amount'
                return
            one_din = self.rate
            if self.rate == 0:
                self.ids.result_label.theme_text_color = 'Error'
                self.ids.result_label.text = self.error
                return
            amount = round(customer_input * one_din, 2)
            self.ids.result_label.text = f'{self.ids.input.text} RSD is: [color=#e87b27]{amount} EUR[/color]'

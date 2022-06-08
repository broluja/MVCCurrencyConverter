from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

from View.Managers.currency_manager import CurrencyManager


class FirstScreenView(MDScreen):
    menu_list = ListProperty()
    menu = ObjectProperty()
    error = StringProperty('')
    dropdown_list = ListProperty()
    rate = NumericProperty()

    def __init__(self, **kwargs):
        super(MDScreen, self).__init__(**kwargs)
        if not self.menu_list:
            CurrencyManager().get_list_currencies(self.on_server_data, self.on_server_failure)

    def on_server_data(self, data):
        self.menu_list = data

    def on_server_failure(self, error):
        self.error = error
        self.ids.result.theme_text_color = 'Error'
        self.ids.result.text = self.error

    def open_menu_one(self):
        for ids, abbreviation, symbol in self.menu_list:
            self.dropdown_list.append(
                {'viewclass': 'OneLineListItem',
                 'text': f'{ids} - {abbreviation} - {symbol}',
                 'on_press': lambda x=f'{ids} - {symbol}': self.option_callback(x)}
            )
        self.menu = MDDropdownMenu(width_mult=4)
        self.menu.caller = self.ids.drop_item_one
        self.menu.items = self.dropdown_list
        self.menu.open()

    def open_menu_two(self):
        for ids, abbreviation, symbol in self.menu_list:
            self.dropdown_list.append(
                {'viewclass': 'OneLineListItem',
                 'text': f'{ids} - {abbreviation} - {symbol}',
                 'on_press': lambda x=f'{ids} - {symbol}': self.option_callback(x)}
            )
        self.menu = MDDropdownMenu(width_mult=4)
        self.menu.caller = self.ids.drop_item_two
        self.menu.items = self.dropdown_list
        self.menu.open()

    def option_callback(self, x):
        self.menu.caller.text = str(x)
        self.menu.dismiss()

    def buy_money(self):
        from_value = self.ids.drop_item_one.text[:3]
        to_value = self.ids.drop_item_two.text[:3]
        if not from_value.isupper():
            self.ids.result.text = 'Please choose FROM currency'
            return
        if not to_value.isupper():
            self.ids.result.text = 'Please choose TO currency'
            return
        try:
            amount = float(self.ids.amount_input.text)
            self.get_rate()
            multiplier = self.rate
            result = round(multiplier * amount, 2)
            self.ids.result.text = f'For {amount} {from_value}\n you get {result} {to_value}'
        except ValueError:
            self.ids.result.text = 'Please enter valid amount!'
        except Exception as e:
            print(e.args)
            result = 'Something went wrong. Try again'
            self.ids.result.text = result

    def get_exchange_rate(self, from_currency, to_currency):
        CurrencyManager().get_exchange_rate(from_currency, to_currency, self.on_rate_success, self.on_rate_failure)

    def on_rate_success(self, rate):
        self.rate = rate

    def on_rate_failure(self, error):
        self.rate = 0
        self.error = error

    def get_rate(self):
        from_value = self.ids.drop_item_one.text[:3]
        to_value = self.ids.drop_item_two.text[:3]
        self.get_exchange_rate(from_value, to_value)

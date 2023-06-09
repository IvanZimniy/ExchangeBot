import requests
import json
from config import currency


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_pice(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException('Вводимые валюты не должны быть одинаковыми.\nПосмотреть правила: /help')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f'Валюта "{base}" не найдена в списке валют.\nПосмотреть списко валют: /values')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f'Валюта "{quote}" не найдена в списке валют.\nПосмотреть списко валют: /values')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Количество валюты должно быть указано цифрой. Введенное значение - {amount}.\n \
Посмотреть правила: /help')

        req = requests.get(f'https://v6.exchangerate-api.com/v6/83ccee860d55b6324506ef2b/latest/{base_ticker}')
        req = json.loads(req.content)
        quote_value = req['conversion_rates'][quote_ticker]
        convert_result = quote_value * amount

        return convert_result

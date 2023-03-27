import requests
import json
from config import keys

class APIException(Exception):
    pass

class Convert:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = keys[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        payload = {}
        headers = {
            "apikey": "vxiG1uZ6KozL9tYv8mC8jRqilciWonUa"
        }
        url = f'https://api.apilayer.com/exchangerates_data/latest?symbols={sym_key}&base={base_key}'

        r = requests.get(url, headers=headers, data=payload)
        resp = json.loads(r.content)

        new_price = resp['rates'][sym_key] * amount
        new_price = round(new_price, 3)
        message = f'Цена {amount} {base} в {sym} : {new_price}'

        return message



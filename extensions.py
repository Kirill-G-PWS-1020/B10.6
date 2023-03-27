import requests
import json
from config import exchanges

class APIException(Exception):
    pass

class Convert:
    @staticmethod
    def get_price(base='доллар', sym='рублей', amount=2):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
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

        r = requests.get(f'https://api.apilayer.com/exchangerates_data/latest?symbols={sym_key}&base={base_key}', headers=headers, data=payload)
        resp = json.loads(r.content)
        print(resp)

        new_price = resp['rates'][sym_key] * amount
        new_price = round(new_price, 3)
        message = f'Цена {amount} {base} в {sym} : {new_price}'

        return message



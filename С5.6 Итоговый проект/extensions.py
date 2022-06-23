import json
import requests
from config import exchanges
from config import API_KEY

class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, to_cur, amount):
        try:
            base_key = exchanges[base.lower().lstrip()]
        except KeyError:
            raise APIException(f'Валюта {base} не найдена!')

        try:
            to_cur_key = exchanges[to_cur.lower().lstrip()]
        except KeyError:
            raise APIException(f'Валюта {to_cur} не найдена!')

        if base_key == to_cur_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')
        url = f'https://free.currconv.com/api/v7/convert?q={base_key}_{to_cur_key}' \
              f'&compact=ultra&apiKey={API_KEY}'
        r = requests.get(url)
        resp = json.loads(r.content)
        new_price = resp[f'{base_key}_{to_cur_key}'] * amount
        new_price = round(new_price, 3)
        message =  f'Цена {amount} {base} в {to_cur} : {new_price}'
        return message

import json
from datetime import datetime

from api.tesouro import BuySell


class DataProcess:
    @staticmethod
    def load_last_day(file):
        with open(file, 'rt') as f:
            file = json.loads(f.read())

        if file.get('xlsLastUpdated'):
            return file

    @staticmethod
    def load_current_day():
        bs = BuySell()
        buy, sell = bs.get_price_rate()
        return buy, sell

    @classmethod
    def format_new_data(cls, last_day, buy, sell):
        global bid, ask, puc, puv
        new_data = {}

        for ld in last_day:
            primary_key = ld
            if primary_key != 'xlsLastUpdated':

                try:
                    bid = buy[primary_key]['rate']
                    ask = sell[primary_key]['rate']
                    puc = buy[primary_key]['price']
                    puv = sell[primary_key]['price']
                except:
                    bid = 0
                    ask = sell[primary_key]['rate']
                    puc = 0
                    puv = sell[primary_key]['price']
                finally:
                    new_data[primary_key] = {
                        'date': datetime.today().strftime('%Y-%m-%d'),
                        'bid': bid,
                        'ask': ask,
                        'puc': puc,
                        'puv': puv,
                        'txm': (bid + ask) / 2,
                        'pum': (puc + puv) / 2
                    }

        return new_data


if __name__ == '__main__':
    last_day = DataProcess().load_last_day('../lastDay.json')
    buy, sell = DataProcess().load_current_day()

    new_data = DataProcess().format_new_data(last_day, buy, sell)

    print(f'Last Day: {json.dumps(last_day)}')
    print(f'New Day: {json.dumps(new_data)}')
    print(f'Buy: {json.dumps(buy)}')
    print(f'Sell: {json.dumps(sell)}')


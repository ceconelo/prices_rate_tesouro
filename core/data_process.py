import json
from loguru import logger as log
from datetime import datetime

from api.tesouro import BuySell


class DataProcess:
    @staticmethod
    def load_last_day(file):
        log.info('Loading the last day...')
        with open(file, 'rt') as f:
            file = json.loads(f.read())

        if file.get('xlsLastUpdated'):
            return file

    @staticmethod
    def get_current_day():
        log.info('Getting the current day...')
        bs = BuySell()
        buy, sell = bs.get_price_rate()
        return buy, sell

    @staticmethod
    def format_current_day(last_day, buy, sell):
        log.info('Formatting the current day...')
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

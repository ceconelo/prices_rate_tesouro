import json
from loguru import logger as log
from datetime import datetime
from collections import OrderedDict

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

    @staticmethod
    def calcute_variation(current_day, last_day):
        log.info('Calculating the variation...')
        variation = {}
        for key in current_day:
            if key != 'xlsLastUpdated':
                if current_day[key]['bid'] > 0: # only buy bonds
                    variation[key] = {
                        'year': key.split('\t')[1].split('-')[0],
                        'rate': current_day[key]['bid'],
                        'rate_diff': round(100 * (current_day[key]['bid'] - last_day[key]['bid']) / last_day[key]['bid'], 1),
                        'price': current_day[key]['puc'],
                        'price_diff': round(100 * (current_day[key]['puc'] - last_day[key]['puc']) / last_day[key]['puc'], 1),
                    }
        return variation

    @staticmethod
    def aggregate_data(variation):
        log.info('Aggregating the data...')
        buy_bonds = []
        for key, value in variation.items():
            buy_bonds.append({'name': key[:-12], 'value': value})

        od = OrderedDict()

        for bond in buy_bonds:
            od.setdefault(bond['name'], list()).append(
                {'year': bond['value']['year'], 'rate': bond['value']['rate'], 'rate_diff': bond['value']['rate_diff'],
                 'price': bond['value']['price']})

        agg_data = [{k: v.pop() if len(v) == 1 else v} for k, v in od.items()]
        return agg_data



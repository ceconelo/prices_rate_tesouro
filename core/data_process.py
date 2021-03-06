import json
import os
import sys

from loguru import logger as log
from datetime import datetime
from collections import OrderedDict

from api.tesouro import BuySell
from api.utils import fake_file


class DataProcess:

    @classmethod
    def open_file(cls, file):
        with open(file, 'rt') as f:
            file = json.loads(f.read())
        return file

    @staticmethod
    def load_last_day(file):
        """
        if the file doesn't exist, create it using the fake_file variable
        """
        try:
            log.info('Loading the last day...')
            file = DataProcess.open_file(file=file)

            if file.get('xlsLastUpdated'):
                return file
        except BaseException as err:
            log.error(f'The file was not found or is not valid: {file}')
            try:
                log.info('Creating a new file...')
                with open('last_day.json', 'w') as f:
                    f.write(json.dumps(fake_file, indent=2))
            except:
                log.error(f'Error: {err}')
                log.error(f'Occurred an error while creating the file')
            finally:
                log.info('Loading the last day...')
                file = DataProcess.open_file(file=file)

                if file.get('xlsLastUpdated'):
                    return file

    @staticmethod
    def get_current_day():
        log.info('Getting the current day...')
        bs = BuySell()
        buy, sell, last_update = bs.get_price_rate()
        return buy, sell, last_update

    @staticmethod
    def format_current_day(last_day, buy, sell, last_update):
        log.info('Formatting the current day...')
        global bid, ask, puc, puv
        new_data = {}

        for ld in last_day:
            primary_key = ld
            if primary_key != 'xlsLastUpdated':

                try:
                    # Securities to invest
                    bid = buy[primary_key]['rate']
                    ask = sell[primary_key]['rate']
                    puc = buy[primary_key]['price']
                    puv = sell[primary_key]['price']
                except:
                    # Securities to redeem
                    bid = 0
                    ask = sell[primary_key]['rate']
                    puc = 0
                    puv = sell[primary_key]['price']
                finally:
                    new_data[primary_key] = {
                        'date': last_update,
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
        """
        Calculate the variation between the current day and the last day
        """
        log.info('Calculating the variation...')
        variation = {}
        for key in current_day:
            if key != 'xlsLastUpdated':
                if current_day[key]['bid'] > 0:  # only buy bonds
                    variation[key] = {
                        'year': key.split('\t')[1].split('-')[0],
                        'rate': current_day[key]['bid'],
                        'rate_diff': round(
                            100 * (current_day[key]['bid'] - last_day[key]['bid']) / last_day[key]['bid'], 1),
                        'price': current_day[key]['puc'],
                        'price_diff': round(
                            100 * (current_day[key]['puc'] - last_day[key]['puc']) / last_day[key]['puc'], 1),
                    }
        return variation

    @staticmethod
    def aggregate_data(variation):
        """
        Aggregate the data to a single list aggregated by name of the bond.
        """
        log.info('Aggregating the data...')
        buy_bonds = []
        for key, value in variation.items():
            buy_bonds.append({'name': key[:-11], 'value': value})

        od = OrderedDict()

        for bond in buy_bonds:
            od.setdefault(bond['name'], list()).append(
                {'year': bond['value']['year'], 'rate': bond['value']['rate'], 'rate_diff': bond['value']['rate_diff'],
                 'price': bond['value']['price']})

        agg_data = [{k: v.pop() if len(v) == 1 else v} for k, v in od.items()]
        return agg_data

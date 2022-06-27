import requests
from http import HTTPStatus
import os
import sys

from loguru import logger as log
from .utils import format_date

import warnings

warnings.filterwarnings("ignore")


class BuySell:
    @classmethod
    def __parse(cls, response):
        global last_update

        log.info('Parsing the data...')
        buy = {}
        sell = {}

        for trlist in response['response']['TrsrBdTradgList']:
            venc = format_date(trlist['TrsrBd']['mtrtyDt'])
            titulo = trlist['TrsrBd']['nm']
            name = " ".join(titulo.split(" ")[:-1]) + '\t' + venc

            if trlist['TrsrBd']['minInvstmtAmt'] != 0:  # Separando os titulos para compra e resgate
                buy[name] = {
                    'min_invest': trlist['TrsrBd']['minInvstmtAmt'],  # Valor mínimo de investimento
                    'price': float(trlist['TrsrBd']['untrInvstmtVal']),  # Preço unitário
                    'rate': float(trlist['TrsrBd']['anulInvstmtRate']),  # Rentabilidade anual
                    'venc': venc  # Data de vencimento
                }
            sell[name] = {
                'price': float(trlist['TrsrBd']['untrRedVal']),  # Preço unitário
                'rate': float(trlist['TrsrBd']['anulRedRate']),  # Rentabilidade anual
                'venc': venc  # Data de vencimento
            }

        log.info(f'Total of Treasure bonds available to buy: {len(buy)}')
        log.info(f'Total of Treasure bonds available to sell: {len(sell)}')

        # Last update of the information in website
        last_update = format_date(response['response']['TrsrBondMkt']['qtnDtTm'])

        return buy, sell, last_update

    def __init__(self):
        self.__url_base = 'https://www.tesourodireto.com.br/'
        self.__url_target = 'https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/service/api/treasurybondsinfo.json'
        self.__headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }

        log.info('Starting the request...')
        try:
            log.info('Accessing the treasure website')
            self.web = requests.session()
            self.web.get(url=self.__url_base, headers=self.__headers, verify=False)
        except:
            log.error('Error while accessing the website')
            sys.exit(os.EX_UNAVAILABLE)

    def get_price_rate(self):
        response = requests.get(self.__url_target, headers=self.__headers, cookies=self.web.cookies, verify=False)
        log.info('Requesting the data...')
        if response.status_code == HTTPStatus.OK:
            return self.__parse(response.json())
        else:
            log.error('Error while requesting the data')
            sys.exit(os.EX_UNAVAILABLE)


if __name__ == '__main__':
    import json

    td = BuySell()
    buy, sell = td.get_price_rate()
    print(json.dumps(buy))
    print(json.dumps(sell))

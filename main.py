import json

from loguru import logger as log

from api.tesouro import BuySell
from core.data_process import DataProcess


def main():
    last_day = DataProcess.load_last_day('lastDay.json')
    buy, sell = DataProcess.get_current_day()
    current_day = DataProcess.format_current_day(last_day, buy, sell)

    print(f'Last Day: {json.dumps(last_day)}')
    print(f'Current Dat: {json.dumps(current_day)}')
    print(f'Buy: {json.dumps(buy)}')
    print(f'Sell: {json.dumps(sell)}')


if __name__ == '__main__':
    log.info('Initializing...')
    main()

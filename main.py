import json
import os
import sys

from datetime import datetime
from loguru import logger as log

from api.tesouro import BuySell
from core.data_process import DataProcess


def prepare_to_publish(agg_data):
    log.info('Preparing text to publish...')
    for bound in agg_data:
        try:
            for key, values in bound.items():
                log.info(f'{key}')
                tweet_done_to_publish = f'{key}\nBrazilian sovereign inflation-linked bonds: coupons\n'
                try:
                    values = sorted(values, key=lambda x: x['year'])
                    for value in values:
                        tweet_done_to_publish += f'{value["year"]} {value["rate"]}% ({value["rate_diff"]}%)\n'
                except:
                    tweet_done_to_publish += f'{values["year"]} {values["rate"]}% ({values["rate_diff"]}%)\n'
                yield tweet_done_to_publish
        except BaseException as err:
            log.error(f'Error on {bound}')
            log.error(f'Error: {err}')
            log.error(f'Occurred an error while preparing the text to publish')


def main():
    last_day = DataProcess.load_last_day(file='lastDay.json')
    buy, sell = DataProcess.get_current_day()
    current_day = DataProcess.format_current_day(last_day=last_day, buy=buy, sell=sell)
    variation = DataProcess.calcute_variation(current_day=current_day, last_day=last_day)
    agg_data = DataProcess.aggregate_data(variation=variation)
    tweet_done_to_publish = prepare_to_publish(agg_data=agg_data)

    log.debug(f'Last Day: {json.dumps(last_day)}')
    log.debug(f'Current Day: {json.dumps(current_day)}')
    log.debug(f'Variation: {json.dumps(variation)}')
    log.debug(f'Buy: {json.dumps(buy)}')
    log.debug(f'Sell: {json.dumps(sell)}')

    for tweet in tweet_done_to_publish:
        try:
            log.info(f'Publishing tweet: {tweet}')
            # post tweet
            print(tweet)
        except BaseException as err:
            log.error(f'Error: {err}')
            log.error(f'There was an error trying to post to twitter.')
            sys.exit(os.EX_OSERR)
    try:
        log.info('Saving the current day...')
        current_day['xlsLastUpdated'] = datetime.today().strftime('%Y-%m-%d')
        current_day = json.dumps(current_day, indent=2)
        with open('last_day.json', 'wt') as f:
            f.write(current_day)
    except BaseException as err:
        log.error(f'Error: {err}')
        log.error(f'There was an error trying to save the last_day file.')
        sys.exit(os.EX_OSERR)


if __name__ == '__main__':
    log.info('Initializing...')
    main()

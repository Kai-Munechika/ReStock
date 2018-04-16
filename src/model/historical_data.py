import json
import time

import requests

from src.config import IEXAPI


# We want historical data to be in the form List[List[epoch time
# (in milliseconds), stock price value]] for charting
class HistoricalData:
    data_sources = {'IEX'}

    def __init__(self, data_source, epoch_as_ms):
        assert data_source in self.data_sources
        self.data_source = data_source
        self.epoch_as_ms = epoch_as_ms

    def get_historical_data(self, symbol):
        """
        :param symbol: stock's ticker symbol
        :return: historical data
        """
        if self.data_source == 'IEX':
            url = '{}/stock/{}/chart/5y'.format(IEXAPI.URL, symbol)
            r = requests.get(url)
            as_list_of_dicts = json.loads(r.text)

            historical_data = [[self.date_time_to_epoch(day['date']),
                                day['close']] for day in as_list_of_dicts]
            return historical_data

        else:
            raise ValueError('Invalid data source')

    def date_time_to_epoch(self, date_time):
        # date_time strings from iex api are of the form yyyy-mm-dd

        _format = ''

        if self.data_source == 'IEX':
            _format = '%Y-%m-%d'

        t = time.strptime(date_time, _format)
        result = int(time.mktime(time.strptime(date_time, _format)))

        if self.epoch_as_ms:
            return result * 1000

        return result

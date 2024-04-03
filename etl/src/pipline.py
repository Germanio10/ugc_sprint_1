from datetime import datetime
import time

from transformer import Transformer
from extractor import Extractor
from loader import Loader
from logger import logger
from state.models import State


STATE_KEY = 'last_produce_time'


class ETL:
    def __init__(self, extractor: Extractor, loader: Loader) -> None:
        self.extractor = extractor
        self.loader = loader

    def run(self, state: State):
        while True:
            new_messages, last_modified = self.extractor.extract(
                self._get_last_time(state))
            if not new_messages:
                state.set_state(STATE_KEY, last_modified.strftime(
                    '%Y-%m-%dT%H:%M:%S.%f'))
                time.sleep(10)
                continue
            events, count = Transformer.transform(new_messages)
            self.loader.load(events)
            logger.info('{} events was uploaded'.format(count))
            print(f'{count} events was uploaded')

    def _get_last_time(self, state: State) -> datetime:
        if state.get_state(STATE_KEY):
            try:
                return datetime.strptime(state.get_state(STATE_KEY), '%Y-%m-%dT%H:%M:%S.%f')
            except ValueError:
                return datetime.min
        return datetime.min

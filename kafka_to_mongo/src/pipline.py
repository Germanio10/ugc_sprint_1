import time

from transformer import Transformer
from extractor import Extractor
from loader import Loader
from logger import logger


STATE_KEY = 'last_produce_time'


class ETL:
    def __init__(self, extractor: Extractor, loader: Loader) -> None:
        self.extractor = extractor
        self.loader = loader

    def run(self):
        while True:
            new_messages = self.extractor.extract()
            if not new_messages:
                time.sleep(10)
                continue
            data, count = Transformer.transform(new_messages)
            self.loader.load(data)
            self.extractor.commit()
            logger.debug('{} data was uploaded'.format(count))
            print(f'{count} data was uploaded')

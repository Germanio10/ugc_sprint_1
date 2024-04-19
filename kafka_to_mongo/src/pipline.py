import time

from extractor import Extractor
from loader import Loader
from logger import logger
from transformer import Transformer


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
            logger.info('{} data was uploaded'.format(count))

from collections import defaultdict

from models import RatingEvent


models = {
    'rating': RatingEvent
}


class Transformer:

    @staticmethod
    def transform(events: list) -> tuple[dict, int]:
        for event in events:
            for key in ['produce_timestamp', 'event_timestamp']:
                if key in event:
                    del event[key]
            return event, len(events)

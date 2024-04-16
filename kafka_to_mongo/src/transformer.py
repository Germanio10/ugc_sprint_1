from collections import defaultdict

from models import RatingEvent, ReviewsEvent, WatchlistEvent, ReviewsRatingEvent


models = {
    'rating': RatingEvent,
    'watchlist': WatchlistEvent,
    'reviews': ReviewsEvent,
    'reviews_rating': ReviewsRatingEvent,
}


class Transformer:

    @staticmethod
    def transform(events: list) -> tuple[dict, int]:
        for event in events:
            for key in ['produce_timestamp', 'event_timestamp']:
                if key in event:
                    del event[key]
        return event, len(events)

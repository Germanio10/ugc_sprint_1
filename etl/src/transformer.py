from collections import defaultdict

from models import FilmQualityEvent, ClickInfoEvent, FilmProgressEvent, FilterEvent, LikeEvent, RatingRmEvent, WatchlistEvent, ReviewsEvent, WatchlistRmEvent, ReviewsRatingEvent


models = {
    'quality': FilmQualityEvent,
    'click_info': ClickInfoEvent,
    'progress': FilmProgressEvent,
    'filter': FilterEvent,
    'rating': LikeEvent,
    'rating_rm': RatingRmEvent,
    'watchlist': WatchlistEvent,
    'watchlist_rm': WatchlistRmEvent,
    'reviews': ReviewsEvent,
    'reviews_rating': ReviewsRatingEvent,
}


class Transformer:

    @staticmethod
    def transform(events: list) -> tuple[dict, int]:
        results = defaultdict(list)
        for event in events:
            event_type = event.pop('event_type')
            results[event_type].append(models[event_type](**event))
        return results, len(events)

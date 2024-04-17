from collections import defaultdict

from models import FilmQualityEvent, ClickInfoEvent, FilmProgressEvent, FilterEvent, LikeEvent, RatingRmEvent, AverageRating


models = {
    'quality': FilmQualityEvent,
    'click_info': ClickInfoEvent,
    'progress': FilmProgressEvent,
    'filter': FilterEvent,
    'rating': LikeEvent,
    'rating_rm': RatingRmEvent,
    'average_rating': AverageRating
}


class Transformer:

    @staticmethod
    def transform(events: list) -> tuple[dict, int]:
        results = defaultdict(list)
        for event in events:
            if 'event_type' in event:
                event_type = event.pop('event_type')
                results[event_type].append(models[event_type](**event))
            else:
                results['average_rating'].append(models['average_rating'](**event))
        return results, len(events)

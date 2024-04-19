import json

import pytest
from starlette import status
from testdata.correct_data import (
    CORRECT_CLICK_DATA,
    CORRECT_FILTER_DATA,
    CORRECT_PROGRESS_DATA,
    CORRECT_QUALITY_DATA,
)

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'film_id, quality, event_timestamp, expected_status',
    [
        (
            '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            0,
            '2024-04-04T10:17:40.102Z',
            status.HTTP_201_CREATED,
        ),
        ('1', 0, '2024-04-04T10:17:40.102Z', status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_quality(
    get_token,
    make_post_request,
    consumer_client,
    film_id,
    quality,
    event_timestamp,
    expected_status,
):
    quality_data = {"film_id": film_id, "quality": quality, "event_timestamp": event_timestamp}

    access_token = await get_token()
    response = await make_post_request(
        data=quality_data, method='film_quality/', access_token=access_token
    )

    for _, message in consumer_client.poll(10.0).items():
        message_value = json.loads(message[-1].value)

        assert CORRECT_QUALITY_DATA['quality'] == message_value['quality']
        assert CORRECT_QUALITY_DATA['film_id'] == message_value['film_id']

    assert response['status'] == expected_status


@pytest.mark.parametrize(
    'film_id, watching_time, film_percentage, event_timestamp, expected_status',
    [
        (
            '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            0,
            0,
            '2024-04-04T11:11:12.973Z',
            status.HTTP_201_CREATED,
        ),
        ('1', 0, 0, '2024-04-04T10:17:40.102Z', status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_film_progress(
    get_token,
    make_post_request,
    consumer_client,
    film_id,
    watching_time,
    film_percentage,
    event_timestamp,
    expected_status,
):
    progress_data = {
        "film_id": film_id,
        "watching_time": watching_time,
        "film_percentage": film_percentage,
        "event_timestamp": event_timestamp,
    }
    access_token = await get_token()
    response = await make_post_request(
        data=progress_data, method='watching_film_progress/', access_token=access_token
    )

    for _, message in consumer_client.poll(10.0).items():
        message_value = json.loads(message[-1].value)

        assert CORRECT_PROGRESS_DATA['film_id'] == message_value['film_id']
        assert CORRECT_PROGRESS_DATA['watching_time'] == message_value['watching_time']
        assert CORRECT_PROGRESS_DATA['film_percentage'] == message_value['film_percentage']

    assert response['status'] == expected_status


@pytest.mark.parametrize(
    'url, click_time, time_on_page, event_timestamp, expected_status',
    [
        (
            'string',
            '2024-04-04T11:11:12.973Z',
            0,
            '2024-04-04T13:32:33.807Z',
            status.HTTP_201_CREATED,
        ),
        (1, 0, 0, '2024-04-04T10:17:40.102Z', status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_click_tracking(
    get_token,
    make_post_request,
    consumer_client,
    url,
    click_time,
    time_on_page,
    event_timestamp,
    expected_status,
):
    click_data = {
        "url": url,
        "click_time": click_time,
        "time_on_page": time_on_page,
        "event_timestamp": event_timestamp,
    }
    access_token = await get_token()
    response = await make_post_request(
        data=click_data, method='click_tracking/', access_token=access_token
    )

    for _, message in consumer_client.poll(10.0).items():
        message_value = json.loads(message[-1].value)

        assert CORRECT_CLICK_DATA['url'] == message_value['url']
        assert CORRECT_CLICK_DATA['time_on_page'] == message_value['time_on_page']

    assert response['status'] == expected_status


@pytest.mark.parametrize(
    'genre_id, genre, sort, event_timestamp, expected_status',
    [
        (
            '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            'string',
            'string',
            '2024-04-04T13:32:33.807Z',
            status.HTTP_201_CREATED,
        ),
        ('1', 0, 0, '2024-04-04T10:17:40.102Z', status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_filter(
    get_token,
    make_post_request,
    consumer_client,
    genre_id,
    genre,
    sort,
    event_timestamp,
    expected_status,
):
    click_data = {
        "genre_id": genre_id,
        "genre": genre,
        "sort": sort,
        "event_timestamp": event_timestamp,
    }
    access_token = await get_token()
    response = await make_post_request(
        data=click_data, method='search_filter/', access_token=access_token
    )

    for _, message in consumer_client.poll(10.0).items():
        message_value = json.loads(message[-1].value)

        assert CORRECT_FILTER_DATA['genre_id'] == message_value['genre_id']
        assert CORRECT_FILTER_DATA['genre'] == message_value['genre']
        assert CORRECT_FILTER_DATA['sort'] == message_value['sort']

    assert response['status'] == expected_status

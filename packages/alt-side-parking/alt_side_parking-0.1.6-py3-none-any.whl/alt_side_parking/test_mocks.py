import json
from collections import namedtuple
from unittest.mock import Mock

import automock

Response = namedtuple("Response", "status text")


def tweet_mock_factory(failed_response=False):
    if failed_response:
        response = Response(status=400, text="Bad Query")
        tweets = []
    else:
        response = Response(status=200, text="Good")
        tweets = [
            {
                "contributors": None,
                "coordinates": None,
                "created_at": "Sun Sep 20 20:00:28 +0000 2020",
                "entities": {
                    "hashtags": [{"indices": [0, 7], "text": "NYCASP"}],
                    "symbols": [],
                    "urls": [],
                    "url": "https://t.co/abcdefg",
                },
                "user_mentions": [],
                "favorite_count": 16,
                "favorited": False,
                "geo": None,
                "id": 123232,
                "id_str": "123232",
                "in_reply_to_screen_name": None,
                "in_reply_to_status_id": None,
                "in_reply_to_status_id_str": None,
                "in_reply_to_user_id": None,
                "in_reply_to_user_id_str": None,
                "is_quote_status": False,
                "lang": "en",
                "place": None,
                "possibly_sensitive": False,
                "retweet_count": 9,
                "retweeted": False,
                "source": '<a href="https://www.hootsuite.com" rel="nofollow">Hootsuite Inc.</a>',
                "text": "#NYCASP rules will be in effect tomorrow, Monday, September 21",
                "truncated": False,
                "user": {},
            },
            {
                "contributors": None,
                "coordinates": None,
                "created_at": "Sun Sep 20 06:00:28 +0000 2020",
                "entities": {
                    "hashtags": [{"indices": [0, 7], "text": "NYCASP"}],
                    "symbols": [],
                    "urls": [],
                    "url": "https://t.co/abcdefg",
                },
                "user_mentions": [],
                "favorite_count": 16,
                "favorited": False,
                "geo": None,
                "id": 123232,
                "id_str": "123232",
                "in_reply_to_screen_name": None,
                "in_reply_to_status_id": None,
                "in_reply_to_status_id_str": None,
                "in_reply_to_user_id": None,
                "in_reply_to_user_id_str": None,
                "is_quote_status": False,
                "lang": "en",
                "place": None,
                "possibly_sensitive": False,
                "retweet_count": 9,
                "retweeted": False,
                "source": '<a href="https://www.hootsuite.com" rel="nofollow">Hootsuite Inc.</a>',
                "text": "#NYCASP rules are suspended today, September 20",
                "truncated": False,
                "user": {},
            },
        ]

    def side_effect(url, method, body, headers=None):
        return response, json.dumps(tweets).encode("utf-8")

    m = Mock()
    m().request.side_effect = side_effect
    return m


automock.register("alt_side_parking.sms.get_client")
automock.register("alt_side_parking.feed.get_client", tweet_mock_factory)

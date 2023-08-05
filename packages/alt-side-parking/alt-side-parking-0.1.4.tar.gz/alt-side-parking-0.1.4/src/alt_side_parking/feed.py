import json
from typing import List
from urllib.parse import urlencode

import arrow
import oauth2
import structlog

from .config import (
    NYCASP_TWITTER_ACCOUNT,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
)

logger = structlog.get_logger()

TWEETS_API_URL = "https://api.twitter.com/1.1/statuses/user_timeline.json?"
SUSPENDED_TODAY_TEXT = "#NYCASP rules are suspended today, {today}"


def is_suspended_today() -> bool:
    tweets = get_nyc_alt_side_parking_tweets()
    today = arrow.utcnow().to("US/Eastern")
    return any(
        t.startswith(SUSPENDED_TODAY_TEXT.format(today=today.format("MMMM D")))
        for t in tweets
    )


def get_nyc_alt_side_parking_tweets(count: int = 5) -> List[str]:
    search_query = {
        "count": count,
        "screen_name": NYCASP_TWITTER_ACCOUNT,
    }
    url = TWEETS_API_URL + urlencode(search_query)
    client = get_client()
    response, tweets = client.request(
        url.encode("utf-8"),
        method="GET",
        body="".encode("utf-8"),
        headers=None,
    )
    if response.status != 200:
        logger.error(
            "could not fetch tweets", status=response.status, response=response
        )
        tweets = []
    else:
        tweets = [t["text"] for t in json.loads(tweets.decode("utf-8"))]
    return tweets


def get_client() -> oauth2.Client:
    consumer = oauth2.Consumer(
        key=TWITTER_CONSUMER_KEY, secret=TWITTER_CONSUMER_SECRET
    )
    token = oauth2.Token(
        key=TWITTER_ACCESS_TOKEN, secret=TWITTER_ACCESS_TOKEN_SECRET
    )
    return oauth2.Client(consumer, token)

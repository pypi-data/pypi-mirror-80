"""Faust app"""

import logging
import random
import uuid
from datetime import datetime

import faust

from domination.shadow import ShaDow


class HumanRating(faust.Record, serializer='json', include_metadata=False):
    """Source object from topic 'dominate'"""
    rating: int
    unique_id: str


class HumanCategorized(faust.Record, serializer='json', include_metadata=False):
    """Computed object sent to topic 'shadow'"""
    type: str
    unique_id: str
    emit_timestamp: datetime


app = faust.App(
    'dominate-the-world',
    broker='kafka://localhost:9092',
)

dominate_topic = app.topic('dominate', value_type=HumanRating)
shadow_topic = app.topic('shadow', value_type=HumanCategorized)


def process_human_rating(human_rating: HumanRating) -> str:
    """Returns rating for one human"""
    if isinstance(human_rating.rating, int):
        return ShaDow().worker(human_rating.rating)
    else:
        raise ValueError('human rating is not an integer')


@app.agent(dominate_topic)
async def detect_human_type(human_ratings):
    """Agent categorizing humans from topic 'dominate'
     and send results to topic 'shadow'"""
    async for human_rating in human_ratings:
        try:
            evaluation = process_human_rating(human_rating)
            await shadow_topic.send(value=HumanCategorized(
                unique_id=human_rating.unique_id,
                type=evaluation,
                emit_timestamp=datetime.now()
            ))
        except ValueError as err:
            logging.error('Error: %s', str(err))
        yield human_rating


@app.timer(10)
async def producer_of_humans():
    """Agent producing human rating and send result to topic 'dominate'"""
    for _ in range(10):
        await dominate_topic.send(value=HumanRating(
            rating=random.randint(0, 100),
            unique_id=str(uuid.uuid4())
        ))


if __name__ == '__main__':
    app.main()

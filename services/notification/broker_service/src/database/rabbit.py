from typing import Optional
import pika

rq: Optional[pika.BlockingConnection] = None


async def get_rabbit() -> pika.BlockingConnection:
    return rq

import asyncio
import logging
import os
import traceback
from dataclasses import dataclass
from functools import partial
from uuid import UUID
from typing import Literal

import aiohttp
import simplejson as json
from aio_pika import connect, IncomingMessage, Exchange, Message

logger = logging.getLogger('')

STATE_SERVICE_URL = os.getenv('STATE_SERVICE_URL')
STATE_SERVICE_TOKEN = os.getenv('STATE_SERVICE_TOKEN')
STATE_SERVICE_MOCK = os.getenv('STATE_SERVICE_MOCK')

STATE_SERVICE_DEPLOYING_STATE = 'deploying'


class StateServiceException(Exception):
    pass


@dataclass
class OrderAction:
    order: UUID
    action: UUID
    graph: UUID


if not STATE_SERVICE_URL and not os.getenv('DEBUG'):
    raise StateServiceException('Configuration error, STATE_SERVICE_URL required')


async def _make_request(url, data: dict):
    headers = {}
    if STATE_SERVICE_TOKEN:
        headers['Authorization'] = f'Token {STATE_SERVICE_TOKEN}'

    if STATE_SERVICE_MOCK:
        return {}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, json=data) as response:
            if response.status == 400:
                raise StateServiceException(await response.json())
            elif response.status != 201:
                raise StateServiceException(f'State service request error ({response.status}): {await response.text()}')


async def add_action_event(*, action: OrderAction, type, status='', data=None):
    data = {
        'type': type,
        'status': status,
        'data': data
    }
    data.update(action.__dict__)
    await _make_request(
        url=f'{STATE_SERVICE_URL}/action/',
        data=data
    )


async def add_event(*, action: OrderAction, type, status='', data=None, parent=None):
    data = {
        'type': type,
        'status': status,
        'data': data,
        'parent': parent
    }
    data.update(action.__dict__)
    await _make_request(
        url=f'{STATE_SERVICE_URL}/event/',
        data=data
    )


def state_action_decorator(func):
    async def wrapper(*, order_action: OrderAction, node, action_type: Literal['run', 'rollback'] = 'run', **kwargs):
        await add_action_event(
            action=order_action,
            type=STATE_SERVICE_DEPLOYING_STATE,
            status=f'{node}:{action_type}:started',
            data=kwargs
        )
        try:
            result = await func(
                **kwargs,
                order_action=order_action,
                node=node,
                action_type=action_type)
            status = f'{node}:{action_type}:completed'
        except Exception as e:
            result = {'error': str(e), 'traceback': traceback.format_exc()}
            status = f"{node}:{action_type}:error"
            from pprint import pprint
            pprint(traceback.format_exc())
        await add_action_event(
            action=order_action,
            type=STATE_SERVICE_DEPLOYING_STATE,
            status=status,
            data=result
        )
        return result
    return wrapper


class EventsReceiver:
    def __init__(self, fn, mq_addr, mq_input_queue):
        self.mq_addr = mq_addr
        self.input_queue = mq_input_queue
        self.fn = state_action_decorator(fn)

    async def on_message(self, message: IncomingMessage, exchange: Exchange):
        with message.process():
            data = json.loads(message.body)
            if not isinstance(data, dict):
                raise StateServiceException('Invalid message (need struct): %s', data)
            response = await self.fn(
                order_action=OrderAction(
                    order=data.pop('_order_id'),
                    action=data.pop('_action_id'),
                    graph=data.pop('_graph_id')),
                node=data['_name'],
                action_type=data.get('_type'),  # "run" default
                **data
            )
            await exchange.publish(
                Message(body=json.dumps(response).encode(), content_type="application/json",
                        correlation_id=message.correlation_id),
                routing_key=message.reply_to,
            )

    async def _receive(self, loop, addr, queue_name, queue_kwargs, prefetch_count=None):
        connection = await connect(addr, loop=loop)
        channel = await connection.channel()
        if prefetch_count:
            await channel.set_qos(prefetch_count=prefetch_count)
        queue = await channel.declare_queue(queue_name, **(queue_kwargs or {}))
        await queue.consume(partial(self.on_message, exchange=channel.default_exchange))

    def run(self, queue_kwargs: dict = None, prefetch_count: int = None):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self._receive(
            loop, addr=self.mq_addr, queue_name=self.input_queue,
            queue_kwargs=queue_kwargs,
            prefetch_count=prefetch_count
        ))
        loop.run_until_complete(task)
        logger.info('Awaiting events')
        loop.run_forever()

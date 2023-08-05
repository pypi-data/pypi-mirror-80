State service tools

    Need STATE_SERVICE_URL & STATE_SERVICE_TOKEN (opt) in env.
    Use var STATE_SERVICE_MOCK to emulate state service

Usage:

```python
from typing import Literal
from state_service_utils import EventsReceiver, OrderAction, add_event


async def test_f(*, order_action: OrderAction, node: str, action_type: Literal['run', 'rollback'], **kwargs):
    print(f"New event: {kwargs}")
    await add_event(action=order_action, type='vm', status='created', data={'ip': '10.36.134.123', 'flavor': 'large'})
    return {'success': True}


if __name__ == '__main__':
    EventsReceiver(test_f, mq_addr='amqp://guest:guest@localhost/', mq_input_queue='test-queue').run()
```
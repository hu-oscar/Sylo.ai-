import asyncio

from api.events import EventBus


def test_stream_replays_events_after_last_event_id():
    async def replay():
        bus = EventBus()
        bus.publish("risk.scored", "pay_1", "uetr_1", "1", {"score": 20})
        bus.publish("route.selected", "pay_1", "uetr_1", "1", {"route": "R3"})
        stream = bus.stream(last_event_id=1)
        event = await anext(stream)
        await stream.aclose()
        return event

    event = asyncio.run(replay())
    assert event["id"] == 2
    assert event["type"] == "route.selected"

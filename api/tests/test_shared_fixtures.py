import json
from pathlib import Path

from shared.types import EventEnvelope, Payee, PaymentOrder, RiskContext, RiskResult

FIXTURES = Path(__file__).parents[2] / "shared" / "fixtures"


def test_scene_fixtures_validate_against_shared_types():
    for name in ("scene1.json", "scene2.json"):
        fixture = json.loads((FIXTURES / name).read_text())
        PaymentOrder.model_validate(fixture["order"])
        Payee.model_validate(fixture["payeeRegistry"])
        RiskContext.model_validate(fixture["riskContext"])
        RiskResult.model_validate(fixture["expectedRisk"])


def test_event_stream_fixtures_validate_against_envelope():
    for name in (
        "events-scene1.jsonl",
        "events-scene2.jsonl",
        "events-scene2b.jsonl",
    ):
        lines = (FIXTURES / name).read_text().splitlines()
        assert lines
        for line in lines:
            EventEnvelope.model_validate_json(line)

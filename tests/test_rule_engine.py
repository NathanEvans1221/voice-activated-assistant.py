from pathlib import Path

import pytest

from src.rule_engine import RuleEngine


RULES_PATH = Path(__file__).resolve().parents[1] / "config" / "rules.json"


@pytest.mark.parametrize(
    ("transcript", "rule_id", "response"),
    [
        ("謝謝你的幫忙", "thanks", "不客氣，很高興能幫上忙。"),
        ("我要先說再見", "farewell", "好的，再見！需要幫忙時隨時叫我。"),
        ("我該睡了，晚安", "goodnight", "晚安，祝你今晚有個好夢。"),
        ("請問你叫什麼名字", "identity", "我是你的語音助理，可以依照設定回答問題。"),
        (
            "你能幫我什麼",
            "capabilities",
            "目前我能回應問候、天氣和時間等已設定的情境；天氣與時間回覆是預先設定的內容。",
        ),
    ],
)
def test_added_conversation_scenarios_return_configured_responses(
    transcript, rule_id, response
):
    engine = RuleEngine(str(RULES_PATH))
    engine.load_rules()

    result = engine.match(transcript)

    assert result is not None
    assert result.rule_id == rule_id
    assert result.text == response


def test_generic_agreement_does_not_trigger_greeting():
    engine = RuleEngine(str(RULES_PATH))
    engine.load_rules()

    assert engine.match("好") is None


def test_lower_priority_number_wins_when_multiple_rules_match():
    engine = RuleEngine(str(RULES_PATH))
    engine.load_rules()

    result = engine.match("你好，請幫助我")

    assert result is not None
    assert result.rule_id == "greeting"
    assert result.text == "你好，我是語音助理"

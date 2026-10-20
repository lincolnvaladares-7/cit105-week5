"""Offline parser tests. No API calls are made."""

from extract import parse_response

CLEAN = '[{"title":"Build dashboard","priority":"high","estimate":4}]'
EXPECTED = [
    {"title": "Build dashboard", "priority": "high", "estimate": 4}
]


def test_clean_json():
    assert parse_response(CLEAN) == EXPECTED


def test_markdown_fence():
    assert parse_response(f"```json\n{CLEAN}\n```") == EXPECTED


def test_friendly_sentence():
    assert parse_response(f"Here are your tasks:\n{CLEAN}") == EXPECTED


def test_no_json():
    assert parse_response("Sorry, no tasks available.") == []


def test_cut_off_json():
    assert parse_response('[{"title":"Build dashboard","priority":') == []


def test_invalid_priority():
    text = '[{"title":"Task","priority":"urgent","estimate":2}]'
    assert parse_response(text) == []


def test_missing_key():
    text = '[{"title":"Task","priority":"high"}]'
    assert parse_response(text) == []


def test_invalid_estimate():
    text = '[{"title":"Task","priority":"high","estimate":true}]'
    assert parse_response(text) == []

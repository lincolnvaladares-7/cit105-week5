"""Offline formatting tests using a saved API-shaped sample."""
import json
from pathlib import Path
from fetch_data import format_country


def load_sample():
    return json.loads((Path(__file__).parent / 'sample_country.json').read_text(encoding='utf-8'))


def test_country_fields():
    output = format_country(load_sample())
    assert 'Brazil' in output
    assert 'Brasília' in output
    assert '203,062,512' in output
    assert 'Portuguese' in output
    assert 'BR' in output


def test_missing_fields_do_not_crash():
    output = format_country({'name': {'common': 'Example'}})
    assert 'Example' in output
    assert output.count('Unknown') == 5


def test_empty_data():
    assert 'Unknown' in format_country({})

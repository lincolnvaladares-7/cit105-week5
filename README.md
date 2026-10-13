# CIT 105 — Module 5 — Public API Consumption

**Student:** Lincoln Guimaraes Valadares  
**Project:** `cit105-week5`

## API

- **Name:** REST Countries
- **Endpoint:** `https://restcountries.com/v3.1/name/{country}?fields=name,capital,region,population,languages,cca2`
- **Authentication:** No API key required
- **Extracted fields:** common name, capital, region, population, languages, two-letter country code (six fields)

## Setup and usage

```bash
python -m pip install -r requirements.txt
python fetch_data.py Brazil
python fetch_data.py
python -m pytest -v
```

The optional command-line country argument can be omitted to enter a country interactively. The API request always uses `requests.get(..., timeout=...)`. Status codes are checked before JSON parsing. The network operation is isolated in `fetch_country()`; `format_country()` uses only data and can be tested offline.

## Failure Modes

**These are capture instructions, not fabricated execution results.** Run the commands below on your own machine and replace each `PASTE ACTUAL OUTPUT HERE` block with the exact terminal output, including the message printed by the program. For the offline test, disable Wi-Fi and disconnect Ethernet first, then reconnect after the test.

### Bad path (HTTP 404)

```bash
python fetch_data.py Brazil --base-url https://restcountries.com/v3.1/invalid-path/
```

Actual output:

```text
PASTE ACTUAL OUTPUT HERE
```

### Timeout

```bash
python fetch_data.py Brazil --timeout 0.000001
```

Actual output (if the request happens to complete, rerun or use a slower connection; do not claim a timeout that did not occur):

```text
PASTE ACTUAL OUTPUT HERE
```

### No network

```bash
python fetch_data.py Brazil
```

Actual output (with internet disconnected):

```text
PASTE ACTUAL OUTPUT HERE
```

## Error handling

- `200`: parse and format JSON.
- `404`: show a country-not-found message.
- `500–599`: show a server-problem message.
- Other HTTP codes: show a general HTTP status message.
- Timeout, connection failure, and other `requests.exceptions.RequestException` failures each have user-friendly handling.
- Invalid JSON, unexpected response shapes, and missing country fields are handled without a crash.

## Tests

`test_fetch_data.py` uses `sample_country.json` as saved example data, so formatting tests never call the live API. Tests cover regular formatting, missing fields, and an empty response object.

## Submission

Submit your public GitHub repository URL after uploading these files and filling in the three actual failure outputs.

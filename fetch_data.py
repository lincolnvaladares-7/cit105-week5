
"""CIT 105 Module 5: Public Country API Client."""

import argparse
import requests

BASE_URL = "https://countries.dev/name/"


def fetch_country(country, timeout=5, base_url=BASE_URL):
    """Fetch live country information with error handling."""
    try:
        response = requests.get(
            base_url + requests.utils.quote(country, safe=""),
            timeout=timeout
        )

        if response.status_code == 404:
            return None, "Country not found (404). Check the spelling and try again."

        if 500 <= response.status_code <= 599:
            return None, "The country service is having problems (server error). Try again later."

        if response.status_code != 200:
            return None, f"The country service returned HTTP {response.status_code}. Please try again."

        try:
            data = response.json()
        except ValueError:
            return None, "The country service returned invalid JSON."

        if not isinstance(data, list) or not data or not isinstance(data[0], dict):
            return None, "The country service returned an unexpected response."

        return data[0], None

    except requests.exceptions.Timeout:
        return None, "The country service took too long to respond. Try again."

    except requests.exceptions.ConnectionError:
        return None, "Could not reach the country service. Check your internet connection and try again."

    except requests.exceptions.RequestException:
        return None, "The country request failed. Please try again later."


def format_country(data):
    """Format country data without a network call."""
    if not isinstance(data, dict):
        data = {}

    name = data.get("name") or "Unknown"
    if isinstance(name, dict):
        name = name.get("common") or "Unknown"

    capital = data.get("capital") or "Unknown"
    if isinstance(capital, list):
        capital = ", ".join(map(str, capital)) or "Unknown"

    population = data.get("population")
    population = f"{population:,}" if isinstance(population, int) else "Unknown"

    languages = data.get("languages")
    if isinstance(languages, dict):
        languages = ", ".join(map(str, languages.values())) or "Unknown"
    elif isinstance(languages, list):
        languages = ", ".join(
            str(item.get("name", "Unknown")) if isinstance(item, dict) else str(item)
            for item in languages
        ) or "Unknown"
    else:
        languages = "Unknown"

    fields = [
        ("Name", name),
        ("Capital", capital),
        ("Region", data.get("region") or "Unknown"),
        ("Population", population),
        ("Languages", languages),
        ("Country code", data.get("alpha2Code") or data.get("cca2") or "Unknown"),
    ]

    return "\n".join(
        ["COUNTRY INFORMATION", "-" * 42]
        + [f"{key:<16}: {value}" for key, value in fields]
    )


def main():
    parser = argparse.ArgumentParser(description="Search for country information.")
    parser.add_argument("country", nargs="?", help="Country name")
    parser.add_argument("--timeout", type=float, default=5)
    parser.add_argument("--base-url", default=BASE_URL)
    args = parser.parse_args()

    country = args.country or input("Enter a country name: ").strip()

    if not country:
        print("Please enter a country name.")
        return

    if args.timeout <= 0:
        print("Timeout must be greater than zero.")
        return

    data, error = fetch_country(
        country,
        timeout=args.timeout,
        base_url=args.base_url
    )

    print(error if error else format_country(data))


if __name__ == "__main__":
    main()

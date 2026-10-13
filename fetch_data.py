"""CIT 105 Module 5: public country API client."""
import argparse
import json
import requests

BASE_URL = 'https://restcountries.com/v3.1/name/'
FIELDS = 'name,capital,region,population,languages,cca2'


def fetch_country(country, timeout=5, base_url=BASE_URL):
    """Fetch one country and return (data, user-friendly error)."""
    try:
        response = requests.get(
            base_url + requests.utils.quote(country, safe=''),
            params={'fields': FIELDS}, timeout=timeout
        )
        if response.status_code == 404:
            return None, 'Country not found (404). Check the spelling and try again.'
        if 500 <= response.status_code <= 599:
            return None, 'The country service is having problems (server error). Try again later.'
        if response.status_code != 200:
            return None, f'The country service returned HTTP {response.status_code}. Please try again.'
        try:
            data = response.json()
        except ValueError:
            return None, 'The country service returned invalid JSON. Please try again later.'
        if not isinstance(data, list) or not data or not isinstance(data[0], dict):
            return None, 'The country service returned an unexpected response.'
        return data[0], None
    except requests.exceptions.Timeout:
        return None, 'The country service took too long to respond. Try again.'
    except requests.exceptions.ConnectionError:
        return None, 'Could not reach the country service. Check your internet connection and try again.'
    except requests.exceptions.RequestException:
        return None, 'The country request failed. Please try again later.'


def format_country(data):
    """Format saved country data without making a network call."""
    if not isinstance(data, dict):
        data = {}
    name = data.get('name') or {}
    if not isinstance(name, dict):
        name = {}
    capital = data.get('capital')
    languages = data.get('languages')
    population = data.get('population')
    fields = [
        ('Name', name.get('common') or 'Unknown'),
        ('Capital', ', '.join(map(str, capital)) if isinstance(capital, list) and capital else 'Unknown'),
        ('Region', data.get('region') or 'Unknown'),
        ('Population', f'{population:,}' if isinstance(population, int) else 'Unknown'),
        ('Languages', ', '.join(map(str, languages.values())) if isinstance(languages, dict) and languages else 'Unknown'),
        ('Country code', data.get('cca2') or 'Unknown'),
    ]
    return '\n'.join(['COUNTRY INFORMATION', '-' * 42] + [f'{key:<16}: {value}' for key, value in fields])


def main():
    parser = argparse.ArgumentParser(description='Look up information about a country.')
    parser.add_argument('country', nargs='?', help='Country to search for')
    parser.add_argument('--timeout', type=float, default=5, help='Request timeout in seconds')
    parser.add_argument('--base-url', default=BASE_URL, help='Override endpoint for failure testing')
    args = parser.parse_args()
    country = args.country or input('Enter a country name: ').strip()
    if not country:
        print('Please enter a country name.')
        return
    if args.timeout <= 0:
        print('Timeout must be greater than zero.')
        return
    data, error = fetch_country(country, timeout=args.timeout, base_url=args.base_url)
    print(error if error else format_country(data))


if __name__ == '__main__':
    main()

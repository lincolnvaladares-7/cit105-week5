**API:** countries.dev

**Endpoint:** `https://countries.dev/name/{country}`

**Fields extracted:**
- Name
- Capital
- Region
- Population
- Languages
- Country code

**Testing:** 3 pytest tests passed.

## Failure Modes

### Timeout
```text
The country service took too long to respond. Try again.
```

### No Network
```text
Could not reach the country service. Check your internet connection and try again.
```

### Bad Path (404)
Pending verification with the updated API.

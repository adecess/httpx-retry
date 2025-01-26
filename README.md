# Overview

This is a Python HTTP client based on `httpx.AsyncClient` with an exponential backoff retry strategy resilient to 2 `httpcore.ConnectError`.

## Features

- Async HTTP requests
- Exponential backoff
- Robust error handling

## Exponential Backoff Strategy

Exponential backoff is a retry strategy where wait times between retry attempts increase exponentially.

For example:

- 1st retry: 2^0 = 1 second
- 2nd retry: 2^1 = 2 seconds
- 3rd retry: 2^2 = 4 seconds

More details: [Exponential Backoff (Wikipedia)](https://en.wikipedia.org/wiki/Exponential_backoff)

## Prerequisites

- Python 3.8+
- uv package manager

## Setup

1. Install `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create virtual environment, install dependencies and activate virtual environment:

```bash
uv sync
source .venv/bin/activate  # On Unix/macOS
.venv\Scripts\activate     # On Windows
```

## Running Tests

```bash
pytest -sv tests/
```

## Running Main

```bash
uv run main.py
```

## Usage (in the main file)

```python
client = AsyncClientWithRetry(retries=3)
r = await client.request('GET', 'https://www.example.com')
```

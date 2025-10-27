"""HTTP utilities for downloading Formula 1 race and qualifying data."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

import requests
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

LOGGER = logging.getLogger(__name__)
BASE_URL = "https://ergast.com/api/f1"
DEFAULT_LIMIT = 1000

_SESSION: Session | None = None


def _get_session() -> Session:
    """Return a configured requests session with retry support."""

    global _SESSION
    if _SESSION is None:
        session = requests.Session()
        retry = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET",),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        _SESSION = session
    return _SESSION


def _perform_request(endpoint: str, *, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Perform a GET request and return the parsed JSON.

    Args:
        endpoint: Endpoint path relative to the base Ergast API URL.
        params: Optional query parameters to include in the request.

    Returns:
        The parsed JSON payload as a dictionary.

    Raises:
        requests.HTTPError: if the HTTP request is not successful.
    """

    url = f"{BASE_URL}/{endpoint}"
    LOGGER.debug("Requesting %s params=%s", url, params)
    session = _get_session()
    response = session.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_race_results(season: int) -> List[Dict[str, Any]]:
    """Download all race results for a specific season.

    The Ergast API returns sprint results through a dedicated endpoint, so the
    standard results endpoint contains only the main race classification.

    Args:
        season: The target season year (e.g., 2023).

    Returns:
        A list of race objects including classification details.
    """

    payload = _perform_request(f"{season}/results.json", params={"limit": DEFAULT_LIMIT})
    races = payload.get("MRData", {}).get("RaceTable", {}).get("Races", [])
    LOGGER.debug("Fetched %d races for season %s", len(races), season)
    return races


def fetch_qualifying_results(season: int) -> List[Dict[str, Any]]:
    """Download all qualifying results for a specific season.

    Args:
        season: The target season year (e.g., 2023).

    Returns:
        A list of race objects including qualifying classification details.
    """

    payload = _perform_request(f"{season}/qualifying.json", params={"limit": DEFAULT_LIMIT})
    races = payload.get("MRData", {}).get("RaceTable", {}).get("Races", [])
    LOGGER.debug("Fetched %d qualifying sessions for season %s", len(races), season)
    return races

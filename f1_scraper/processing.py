"""Transform Ergast API payloads into pandas DataFrames."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List

import pandas as pd


def _flatten(dictionary: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Flatten nested dictionaries using dot notation keys."""

    items: List[tuple[str, Any]] = []
    for key, value in dictionary.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(_flatten(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def results_to_dataframe(races: Iterable[Dict[str, Any]]) -> pd.DataFrame:
    """Convert race classification payloads into a DataFrame."""

    rows: List[Dict[str, Any]] = []
    for race in races:
        race_info = _flatten({key: race.get(key) for key in race.keys() if key != "Results"})
        for result in race.get("Results", []):
            row = {**race_info, **_flatten(result)}
            rows.append(row)
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.rename(columns={
            "Circuit.Location.locality": "locality",
            "Circuit.Location.country": "country",
            "Circuit.circuitName": "circuitName",
            "Driver.familyName": "driverFamilyName",
            "Driver.givenName": "driverGivenName",
            "Driver.driverId": "driverId",
            "Constructor.name": "constructorName",
        })
    return df


def qualifying_to_dataframe(races: Iterable[Dict[str, Any]]) -> pd.DataFrame:
    """Convert qualifying session payloads into a DataFrame."""

    rows: List[Dict[str, Any]] = []
    for race in races:
        race_info = _flatten({key: race.get(key) for key in race.keys() if key != "QualifyingResults"})
        for result in race.get("QualifyingResults", []):
            row = {**race_info, **_flatten(result)}
            rows.append(row)
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.rename(columns={
            "Circuit.Location.locality": "locality",
            "Circuit.Location.country": "country",
            "Circuit.circuitName": "circuitName",
            "Driver.familyName": "driverFamilyName",
            "Driver.givenName": "driverGivenName",
            "Driver.driverId": "driverId",
            "Constructor.name": "constructorName",
        })
    return df

"""Excel export helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def export_to_excel(
    *,
    race_results: pd.DataFrame,
    qualifying_results: pd.DataFrame,
    output_path: str | Path,
) -> Path:
    """Export race and qualifying DataFrames into a single Excel workbook."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        race_results.to_excel(writer, sheet_name="races", index=False)
        qualifying_results.to_excel(writer, sheet_name="qualifying", index=False)
    return path

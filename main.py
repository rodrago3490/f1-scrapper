"""Command line interface for exporting Formula 1 race data to Excel."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from f1_scraper import (
    export_to_excel,
    fetch_qualifying_results,
    fetch_race_results,
    qualifying_to_dataframe,
    results_to_dataframe,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Formula 1 race and qualifying data")
    parser.add_argument(
        "year",
        type=int,
        help="Season year to download (e.g., 2023)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("f1_results.xlsx"),
        help="Output Excel file path",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level))

    logging.info("Fetching race results for %s", args.year)
    races = fetch_race_results(args.year)
    logging.info("Fetching qualifying results for %s", args.year)
    qualifying = fetch_qualifying_results(args.year)

    logging.info("Transforming data into dataframes")
    races_df = results_to_dataframe(races)
    qualifying_df = qualifying_to_dataframe(qualifying)

    logging.info("Exporting data to %s", args.output)
    export_to_excel(
        race_results=races_df,
        qualifying_results=qualifying_df,
        output_path=args.output,
    )
    logging.info("Export completed successfully")


if __name__ == "__main__":
    main()

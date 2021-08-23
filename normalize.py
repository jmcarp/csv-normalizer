#!/usr/bin/env python

import codecs
import csv
import sys
from typing import Dict

import pendulum


def main():
    buffer = open_stdin_lenient()
    reader = csv.DictReader(buffer)
    writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames)
    writer.writeheader()
    for idx, row in enumerate(reader):
        try:
            normalized = normalize_row(row)
        except Exception as exc:
            print(f"Error normalizing row {idx}: {exc}", file=sys.stderr)
            continue
        writer.writerow(normalize_row(row))


def open_stdin_lenient():
    """Read from stdin, replacing bad values with the UTF-8 replacement character.

    Note: this relies on `codecs.open` accepting a file descriptor as the filename
    instead of the usual string. Borrowed from https://stackoverflow.com/a/53028829.

    Note: normally we would use a context manager to close the file after reading,
    but stdin in a special file and shouldn't be closed.
    """
    return open_lenient(sys.stdin.fileno())


def open_lenient(fd):
    """Read a file descriptor, replacing bad values with the UTF-8 replacement character."""
    return codecs.open(
        fd,
        encoding="utf-8",
        errors="replace",
    )


def normalize_row(row: Dict) -> Dict:
    foo_duration = normalize_duration(row["FooDuration"])
    bar_duration = normalize_duration(row["BarDuration"])
    return {
        "Timestamp": normalize_timestamp(row["Timestamp"]),
        "Address": row["Address"],
        "ZIP": normalize_zip(row["ZIP"]),
        "FullName": normalize_fullname(row["FullName"]),
        "FooDuration": foo_duration,
        "BarDuration": bar_duration,
        "TotalDuration": foo_duration + bar_duration,
        "Notes": row["Notes"],
    }


TIMESTAMP_INPUT_FORMAT = "M/D/YY h:m:s A"
TIMESTAMP_INPUT_TIMEZONE = "US/Pacific"
TIMESTAMP_OUTPUT_TIMEZONE = "US/Eastern"


def normalize_timestamp(
    value: str,
    input_format: str = TIMESTAMP_INPUT_FORMAT,
    input_timezone: str = TIMESTAMP_INPUT_TIMEZONE,
    output_timezone: str = TIMESTAMP_OUTPUT_TIMEZONE,
) -> str:
    timestamp = pendulum.from_format(value, fmt=input_format, tz=input_timezone)
    return timestamp.to_rfc3339_string()


def normalize_zip(value: str) -> str:
    if not value.isnumeric():
        raise ValueError(f"Zip value must be numeric; got {value}")
    if len(value) > 5:
        raise ValueError(
            f"Zip value must have <=5 digits; value {value} has {len(value)}"
        )
    return value.zfill(5)


def normalize_fullname(value: str) -> str:
    return value.upper()


def normalize_duration(value: str) -> float:
    parts = value.split(":")
    if len(parts) != 3:
        raise ValueError(
            f"Duration must include three colon-delimited numbers; value {value} has {len(parts)}"
        )
    hours, minutes, seconds = parts
    return (
        _normalize_hours(parts[0]) * 60 * 60
        + _normalize_minutes(parts[1]) * 60
        + _normalize_seconds(parts[2])
    )


def _normalize_hours(value: str) -> int:
    if value.isnumeric():
        return int(value)
    else:
        raise ValueError(f"Hour value must be numeric; got {value}")


def _normalize_minutes(value: str) -> int:
    if value.isnumeric():
        minutes = int(value)
    else:
        raise ValueError(f"Minute value must be numeric; got {value}")
    if minutes >= 60:
        raise ValueError(f"Minute value must be less than 60; got {value}")
    return minutes


def _normalize_seconds(value: str) -> float:
    try:
        seconds = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Second value must be a float; got {value}")
    if seconds >= 60:
        raise ValueError(f"Second value must be less than 60; got {value}")
    if seconds < 0:
        raise ValueError(f"Second value must be non-negative; got {value}")
    return seconds


if __name__ == "__main__":
    main()

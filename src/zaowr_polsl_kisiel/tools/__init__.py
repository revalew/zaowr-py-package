"""
The `tools` module contains additional utilities for specific tasks.

Functions:

- `find_aruco_dict`: Identifies the ArUco dictionary used in marker detection.

- `measure_perf`: (custom decorator) Measures the performance (execution time) of a function (optionally saves results to a file).

Usage:
Use this module for miscellaneous tools that enhance functionality.
"""

__all__ = [
    "find_aruco_dict",
    "measure_perf",
]

from .find_aruco_dict import find_aruco_dict # find aruco dictionary if we don't know it
from .measure_perf import measure_perf # measure performance (time) of a function (custom decorator with option to save the results to a file)
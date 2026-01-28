"""
Code extracted from an exploratory notebook.

The notebook should only:
- import this module
- call high-level functions
- visualize results

All real logic lives here.
"""

from typing import Iterable


def normalize(values: Iterable[float]) -> list[float]:
    """
    Normalize a sequence of floats to the range [0, 1].

    This is representative of preprocessing logic
    often developed first in notebooks.
    """
    values = list(values)
    min_value = min(values)
    max_value = max(values)

    if min_value == max_value:
        raise ValueError("Cannot normalize constant values")

    return [
        (value - min_value) / (max_value - min_value)
        for value in values
    ]


def run_example() -> None:
    """
    Example entry point that a notebook might call.
    """
    data = [10.0, 12.0, 15.0]
    normalized = normalize(data)
    print(normalized)


if __name__ == "__main__":
    run_example()

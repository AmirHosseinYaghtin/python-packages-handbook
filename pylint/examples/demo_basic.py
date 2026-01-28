"""
This module demonstrates basic Pylint conventions.

It exists to show:
- module and function docstrings
- naming conventions
- simple, lint-clean code
"""

def add(x: int, y: int) -> int:
    """
    Add two integers and return the result.

    This function is intentionally simple.
    """
    return x + y


def main() -> None:
    """
    Entry point for manual execution.
    """
    result = add(2, 3)
    print(result)


if __name__ == "__main__":
    main()

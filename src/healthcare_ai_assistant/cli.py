from __future__ import annotations

import argparse

from .config import load_settings
from .runner import create_runtime


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Healthcare AI Assistant from the command line.")
    parser.add_argument("query", nargs="?", default="Look up Anjali Mehra and summarize her treatment plan.")
    args = parser.parse_args()
    runtime = create_runtime(load_settings())
    print(runtime.run(args.query))


if __name__ == "__main__":
    main()

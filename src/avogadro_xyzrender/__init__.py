"""Avogadro plugin for publication-quality molecular graphics using xyzrender."""

import argparse
import json
import sys


def main():
    # Avogadro calls the plugin as:
    #   avogadro-xyzrender <identifier> [--lang <locale>] [--debug]
    # with the options + molecule JSON on stdin.
    parser = argparse.ArgumentParser()
    parser.add_argument("feature")
    parser.add_argument("--lang", nargs="?", default="en")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    avo_input = json.load(sys.stdin)
    output = None

    match args.feature:
        case "render":
            from .renderer import run_render
            output = run_render(avo_input)
        case "animation":
            from .renderer import run_animation
            output = run_animation(avo_input)

    if output is not None:
        print(json.dumps(output))

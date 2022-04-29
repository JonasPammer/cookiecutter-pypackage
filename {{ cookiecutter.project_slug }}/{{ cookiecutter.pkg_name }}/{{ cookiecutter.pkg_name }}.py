from __future__ import annotations

{%- if cookiecutter.command_line_interface|lower == 'argparse' %}
from typing import Sequence

import argparse
{%- endif %}
{% if cookiecutter.command_line_interface|lower == 'click' %}
import click
{%- endif %}

{% if cookiecutter.command_line_interface|lower == 'click' %}
@click.command()
def main() -> int:
    return 0
{%- endif %}
{%- if cookiecutter.command_line_interface|lower == 'argparse' %}
def main(argv: Sequence[str] | None = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()
    return 0
{%- endif %}


if __name__ == "__main__":
    raise SystemExit(main())

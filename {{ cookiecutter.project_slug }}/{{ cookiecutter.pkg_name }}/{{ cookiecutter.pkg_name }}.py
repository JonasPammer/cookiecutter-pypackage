from __future__ import annotations

{%- if cookiecutter.command_line_interface|lower == 'argparse' %}
import argparse
{%- endif %}

import sys

{%- if cookiecutter.command_line_interface|lower == 'click' %}
import click
{%- endif %}

{% if cookiecutter.command_line_interface|lower == 'click' %}
@click.command()
def main(args=None):
    return 0
{%- endif %}
{%- if cookiecutter.command_line_interface|lower == 'argparse' %}
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()
    return 0
{%- endif %}


if __name__ == "__main__":
    raise SystemExit(main())

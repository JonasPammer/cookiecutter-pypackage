"""Tests for `{{ cookiecutter.project_slug }}` package."""
from __future__ import annotations

{% if cookiecutter.use_pytest == 'y' -%}
import pytest
{%- else %}
import unittest
{%- endif %}
{%- if cookiecutter.command_line_interface|lower == 'click' %}
from click.testing import CliRunner
{%- endif %}

from {{ cookiecutter.pkg_name }} import {{ cookiecutter.pkg_name }}


{%- if cookiecutter.use_pytest == 'y' %}


@pytest.fixture
def response():
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
{%-   if cookiecutter.command_line_interface|lower == 'click' %}


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke({{ cookiecutter.pkg_name }}.main)
    assert result.exit_code == 0
    # assert 'some string' in result.output

{%-   endif %}
{%- else %}


class Test{{ cookiecutter.pkg_name|title }}(unittest.TestCase):
    """Tests for `{{ cookiecutter.pkg_name }}` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
{%- if cookiecutter.command_line_interface|lower == 'click' %}

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke({{ cookiecutter.pkg_name }}.main)
        assert result.exit_code == 0
    # assert 'some string' in result.output
{%- endif %}
{%- endif %}

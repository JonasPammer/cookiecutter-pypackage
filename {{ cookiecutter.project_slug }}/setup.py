"""https://setuptools.pypa.io/en/latest/userguide/declarative_config.html.

If compatibility with legacy builds (those not using the PEP 517 build
API, i.e. pip <19) is desired, a setup.py file containing a setup()
function call is still required even if your configuration resides in
setup.cfg.
"""
from __future__ import annotations

from setuptools import setup

setup()

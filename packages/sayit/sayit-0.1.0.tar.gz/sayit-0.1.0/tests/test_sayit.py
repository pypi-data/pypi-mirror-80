#!/usr/bin/env python

"""Tests for `sayit` package."""

import pytest

from click.testing import CliRunner

from sayit import say
from sayit import cli


@pytest.mark.parametrize(
    "number, human_text",
    [
        (0, "zero"),
        (1, "one"),
        (2, "two"),
        (3, "three"),
        (4, "four"),
        (5, "five"),
        (6, "six"),
        (7, "seven"),
        (8, "eight"),
        (9, "nine"),
    ],
)
def test_single_digit(number, human_text):
    assert say(number) == human_text


@pytest.mark.parametrize(
    "number, human_text",
    [
        (10, "ten"),
        (20, "twenty"),
    ],
)
def test_regular_double_digit(number, human_text):
    assert say(number) == human_text


@pytest.mark.parametrize(
    "number, human_text",
    [
        (21, "twenty one"),
        (45, "forty five"),
        (145, "one hundred forty five"),
        (945, "nine hundred forty five"),
        (42311, "forty two thousand three hundred eleven"),
    ],
)
def test_random_numbers(number, human_text):
    assert say(number) == human_text


# def test_command_line_interface():
#     """Test the CLI."""
#     runner = CliRunner()
#     result = runner.invoke(cli.main)
#     assert result.exit_code == 0
#     assert 'sayit.cli.main' in result.output
#     help_result = runner.invoke(cli.main, ['--help'])
#     assert help_result.exit_code == 0
#     assert '--help  Show this message and exit.' in help_result.output

"""Tests for the CLI serve command."""

from click.testing import CliRunner
from unittest.mock import patch

from linkctl.cli import main


def test_serve_command_exists():
    runner = CliRunner()
    result = runner.invoke(main, ["serve", "--help"])
    assert result.exit_code == 0
    assert "host" in result.output.lower() or "port" in result.output.lower()


def test_serve_command_has_host_option():
    runner = CliRunner()
    result = runner.invoke(main, ["serve", "--help"])
    assert "--host" in result.output


def test_serve_command_has_port_option():
    runner = CliRunner()
    result = runner.invoke(main, ["serve", "--help"])
    assert "--port" in result.output


@patch("linkctl.cli.uvicorn.run")
def test_serve_calls_uvicorn_with_defaults(mock_run):
    runner = CliRunner()
    runner.invoke(main, ["serve"])
    mock_run.assert_called_once()
    call_kwargs = mock_run.call_args
    assert call_kwargs[1]["host"] == "127.0.0.1"
    assert call_kwargs[1]["port"] == 8000


@patch("linkctl.cli.uvicorn.run")
def test_serve_respects_custom_host_port(mock_run):
    runner = CliRunner()
    runner.invoke(main, ["serve", "--host", "0.0.0.0", "--port", "9000"])
    call_kwargs = mock_run.call_args
    assert call_kwargs[1]["host"] == "0.0.0.0"
    assert call_kwargs[1]["port"] == 9000

# Copyright (C) 2020-2023 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""CLI interface tests module."""

from unittest import mock
from unittest import TestCase

from openfl.interface.cli import show_header, review_plan_callback, \
    error_handler, disable_warnings, cli, entry
from openfl.interface.cli import CLI


def test_cli_show_header():
    ret = show_header()
    assert ret is None


@mock.patch('builtins.open', mock.mock_open(read_data='test file'))
@mock.patch('openfl.interface.cli.confirm')
def test_cli_review_plan_callback(mock_confirm):
    mock_confirm.side_effect = [True, False]

    ret1 = review_plan_callback('', '')
    assert ret1 is True

    ret2 = review_plan_callback('', '')
    assert ret2 is False


def test_cli_error_handler():
    with TestCase.assertRaises(test_cli_error_handler, TypeError):
        error_handler('cannot import TensorFlow')

    with TestCase.assertRaises(test_cli_error_handler, TypeError):
        error_handler('cannot import PyTorch')

    with TestCase.assertRaises(test_cli_error_handler, TypeError):
        error_handler('cannot import')


def test_cli_class():
    c = CLI()
    assert isinstance(c, CLI)

    cmds = c.list_commands('')
    assert cmds == {}


@mock.patch('click.core.Command.get_params')
@mock.patch('openfl.interface.cli.CLI.list_commands')
@mock.patch('click.core.Group.get_command')
def test_cli_format_helpe(mock_get_cmd, mock_list_cmds, mock_get_params):
    c = CLI()

    mock_param = mock.Mock()
    mock_get_params.return_value = [mock_param]
    mock_list_cmds.return_value = [mock.Mock()]
    mock_cmd = mock.Mock()
    mock_cmd.name = 'test_name'
    mock_sub = mock.Mock()
    mock_cmd.list_commands.return_value = [mock.Mock()]
    mock_cmd.get_command.return_value = mock_sub
    mock_get_cmd.return_value = mock_cmd

    c.format_help(mock.Mock(), mock.Mock())


def test_cli_disable_warning():
    ret = disable_warnings()
    assert ret is None


@mock.patch('openfl.interface.cli.cli')
@mock.patch('importlib.import_module')
def test_cli_entry(mock_import_module, mock_cli):
    mock_cli.return_value = mock.Mock()
    mock_module = mock.Mock()
    mock_import_module.return_value = mock_module
    mock_module.__getattribute__ = mock.Mock()
    entry()

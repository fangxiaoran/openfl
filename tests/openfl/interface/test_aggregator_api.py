# Copyright (C) 2020-2023 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Aggregator interface tests module."""

from unittest import mock
from unittest import TestCase
from pathlib import Path

from openfl.interface.aggregator import start_


@mock.patch('openfl.interface.aggregator.Plan')
def test_aggregator_start(Plan):
    current_path = Path(__file__).resolve()
    plan_path = current_path.parent.joinpath('plan')
    plan_config = plan_path.joinpath('plan.yaml')
    cols_config = plan_path.joinpath('cols.yaml')

    plan_instance = mock.Mock()
    Plan.parse.return_value = plan_instance
    plan_instance.get_server = mock.Mock()

    start_(['-p', plan_config,
            '-c', cols_config], standalone_mode=False)

    Plan.parse.assert_called_once()


@mock.patch('openfl.interface.aggregator.Plan')
@mock.patch('openfl.interface.aggregator.is_directory_traversal')
def test_aggregator_start_illegal_plan(Plan, mock_is_directory_traversal):
    current_path = Path(__file__).resolve()
    plan_path = current_path.parent.joinpath('plan')
    plan_config = plan_path.joinpath('plan.yaml')
    cols_config = plan_path.joinpath('cols.yaml')

    plan_instance = mock.Mock()
    Plan.parse.return_value = plan_instance
    plan_instance.get_server = mock.Mock()

    mock_is_directory_traversal.side_effect = [True, False]

    with TestCase.assertRaises(test_aggregator_start_illegal_plan, SystemExit):
        start_(['-p', plan_config,
                '-c', cols_config], standalone_mode=False)


@mock.patch('openfl.interface.aggregator.Plan')
@mock.patch('openfl.interface.aggregator.is_directory_traversal')
def test_aggregator_start_illegal_cols(Plan, mock_is_directory_traversal):
    current_path = Path(__file__).resolve()
    plan_path = current_path.parent.joinpath('plan')
    plan_config = plan_path.joinpath('plan.yaml')
    cols_config = plan_path.joinpath('cols.yaml')

    plan_instance = mock.Mock()
    Plan.parse.return_value = plan_instance
    plan_instance.get_server = mock.Mock()

    mock_is_directory_traversal.side_effect = [False, True]

    with TestCase.assertRaises(test_aggregator_start_illegal_cols, SystemExit):
        start_(['-p', plan_config,
                '-c', cols_config], standalone_mode=False)

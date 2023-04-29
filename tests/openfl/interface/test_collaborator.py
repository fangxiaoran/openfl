# Copyright (C) 2020-2023 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Collaborator interface tests module."""

from unittest import mock
from unittest import TestCase
from pathlib import Path

from openfl.interface.collaborator import start_, register_data_path, \
    generate_cert_request_, certify_


@mock.patch('openfl.federated.Plan.parse')
def test_collaborator_start(mock_parse):
    current_path = Path(__file__).resolve()
    plan_path = current_path.parent.joinpath('plan')
    plan_config = plan_path.joinpath('plan.yaml')
    data_config = plan_path.joinpath('data.yaml')

    mock_parse.return_value = mock.Mock()

    ret = start_(['-p', plan_config,
                  '-d', data_config,
                  '-n', 'one'], standalone_mode=False)
    assert ret is None


@mock.patch('openfl.interface.collaborator.is_directory_traversal')
@mock.patch('openfl.federated.Plan.parse')
def test_collaborator_start_illegal_plan(mock_parse, mock_is_directory_traversal):
    current_path = Path(__file__).resolve()
    plan_path = current_path.parent.joinpath('plan')
    plan_config = plan_path.joinpath('plan.yaml')
    data_config = plan_path.joinpath('data.yaml')

    mock_parse.return_value = mock.Mock()
    mock_is_directory_traversal.side_effect = [True, False]

    with TestCase.assertRaises(test_collaborator_start_illegal_plan, SystemExit):
        start_(['-p', plan_config,
                '-d', data_config,
                '-n', 'one'], standalone_mode=False)


@mock.patch('openfl.interface.collaborator.is_directory_traversal')
@mock.patch('openfl.federated.Plan.parse')
def test_collaborator_start_illegal_data(mock_parse, mock_is_directory_traversal):
    current_path = Path(__file__).resolve()
    plan_path = current_path.parent.joinpath('plan')
    plan_config = plan_path.joinpath('plan.yaml')
    data_config = plan_path.joinpath('data.yaml')

    mock_parse.return_value = mock.Mock()
    mock_is_directory_traversal.side_effect = [False, True]

    with TestCase.assertRaises(test_collaborator_start_illegal_plan, SystemExit):
        start_(['-p', plan_config,
                '-d', data_config,
                '-n', 'one'], standalone_mode=False)


@mock.patch('genericpath.isfile')
def test_collaborator_register_data_path(mock_isfile):
    mock_isfile.return_value = True
    ret = register_data_path('one', 'path/data')
    assert ret is None


def test_collaborator_generate_cert_request():
    current_path = Path(__file__).resolve()
    plan_path = current_path.parent.joinpath('plan')
    data_config = plan_path.joinpath('data.yaml')

    ret = generate_cert_request_(['-n', 'one',
                                  '-d', data_config], standalone_mode=False)
    assert ret is None


@mock.patch('openfl.interface.collaborator.is_directory_traversal')
def test_collaborator_generate_cert_request_illegal_path(mock_is_directory_traversal):
    current_path = Path(__file__).resolve()
    plan_path = current_path.parent.joinpath('plan')
    data_config = plan_path.joinpath('data.yaml')

    mock_is_directory_traversal.return_value = True

    with TestCase.assertRaises(test_collaborator_generate_cert_request_illegal_path,
                               SystemExit):
        generate_cert_request_(['-n', 'one',
                                '-d', data_config], standalone_mode=False)


@mock.patch('shutil.unpack_archive')
@mock.patch('os.remove')
@mock.patch('shutil.copy')
@mock.patch('glob.glob')
@mock.patch('openfl.cryptography.io.write_crt')
@mock.patch('openfl.cryptography.ca.sign_certificate')
@mock.patch('click.confirm')
@mock.patch('openfl.cryptography.io.read_crt')
@mock.patch('openfl.cryptography.io.read_key')
@mock.patch('openfl.cryptography.io.read_csr')
def test_collaborator_certify(mock_read_csr, mock_read_key, mock_read_crt,
                              mock_confirm, mock_sign_certificate, mock_write_crt,
                              mock_glob, mock_copy, mock_remove, mock_unarch):
    mock_read_csr.return_value = ['test_csr', 'test_csr_hash']
    mock_read_key.return_value = mock.Mock()
    mock_read_crt.return_value = mock.Mock()
    mock_confirm.return_value = True
    mock_sign_certificate.return_value = mock.Mock()
    mock_write_crt.return_value = mock.Mock()
    mock_glob.return_value = 'test_csr'
    mock_copy.return_value = mock.Mock()
    mock_remove.return_value = mock.Mock()

    ret1 = certify_(['-n', 'one'], standalone_mode=False)
    assert ret1 is None

    current_path = Path(__file__).resolve()
    mock_unarch.return_value = mock.Mock()
    ret2 = certify_(['-n', 'one', '-i', current_path], standalone_mode=False)
    assert ret2 is None

    ret3 = certify_(['-n', 'one', '-s'], standalone_mode=False)
    assert ret3 is None

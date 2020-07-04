import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from sprintd import SprintDaemon
from sprint_config import SprintConfig


def test_sprintd():
    config_text = SprintConfig.slurp_config_file(config.sprint_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000008727242e05ff03271acbb96dee81385e662845353e50618cff84f314253'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'000008727242e05ff03271acbb96dee81385e662845353e50618cff84f314253'

    creds = SprintConfig.get_rpc_creds(config_text, network)
    sprintd = SprintDaemon(**creds)
    assert sprintd.rpc_command is not None

    assert hasattr(sprintd, 'rpc_connection')

    # Sprint testnet block 0 hash == 000008727242e05ff03271acbb96dee81385e662845353e50618cff84f314253
    # test commands without arguments
    info = sprintd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert sprintd.rpc_command('getblockhash', 0) == genesis_hash

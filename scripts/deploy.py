from pathlib import Path

from brownie import Donator, accounts, config, network, project, web3, Contract
from eth_utils import is_checksum_address



def get_src():
    f = open('/home/wavey/contract_source/donator.sol', 'w')
    Donator.get_verification_info()
    f.write(Donator._flattener.flattened_source)
    f.close()
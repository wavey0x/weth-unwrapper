import pytest
import brownie
from brownie import config, Contract, accounts, interface, chain
from brownie import network


def test_operation(unwrapper, ychad, chain, rando):
    starting_eth_balance = ychad.balance()
    treasury = Contract("0x93A62dA5a14C80f265DAbC077fCEE437B1a0Efde")
    yvWeth = Contract("0xa258C4606Ca8206D8aA700cE2143D7db854D168c")
    weth = Contract(yvWeth.token())
    treasury.toGovernance(yvWeth, 4e18, {"from":ychad})         # Send from treasury to ychad
    yvWeth.withdraw({"from":ychad})                      # Withdraw to weth
    amt = weth.balanceOf(ychad)
    weth.approve(unwrapper, 2**256-1, {"from":ychad})
    unwrapper.unwrap(amt,{"from":ychad})
    ending_eth_balance = ychad.balance()
    assert ending_eth_balance > starting_eth_balance
    assert starting_eth_balance + amt == ending_eth_balance

def test_sweep_eth(unwrapper, ychad, chain, rando):
    ychad.transfer(1e18)
    amt = weth.balanceOf(ychad)
    weth.approve(unwrapper, 2**256-1, {"from":ychad})
    unwrapper.unwrap(amt,{"from":ychad})
    ending_eth_balance = ychad.balance()
    assert ending_eth_balance > starting_eth_balance
    assert starting_eth_balance + amt == ending_eth_balance
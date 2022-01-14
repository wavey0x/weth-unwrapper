import pytest
import brownie
from brownie import config, Contract, accounts, interface, chain
from brownie import network


def test_operation(unwrapper, ychad, chain, rando, weth):
    starting_eth_balance = ychad.balance()
    treasury = Contract("0x93A62dA5a14C80f265DAbC077fCEE437B1a0Efde")
    yvWeth = Contract("0xa258C4606Ca8206D8aA700cE2143D7db854D168c")
    weth = Contract(yvWeth.token())
    treasury.toGovernance(yvWeth, 1e18, {"from":ychad})         # Send from treasury to ychad
    yvWeth.withdraw({"from":ychad})                      # Withdraw to weth
    amt = weth.balanceOf(ychad)
    weth.approve(unwrapper, 2**256-1, {"from":ychad})
    unwrapper.unwrap(amt,{"from":ychad})
    ending_eth_balance = ychad.balance()
    assert ending_eth_balance > starting_eth_balance
    assert starting_eth_balance + amt == ending_eth_balance

def test_sweep_eth(unwrapper, ychad, chain, rando, weth):
    ychad.transfer(unwrapper, 1e18)
    eth_bal = unwrapper.balance()
    assert eth_bal > 0
    amt = weth.balanceOf(ychad)
    weth.approve(unwrapper, 2**256-1, {"from":ychad})
    unwrapper.unwrap(amt,{"from":ychad})
    assert eth_bal == unwrapper.balance() # Make sure user got exactly amount they requested
    ychad_before = ychad.balance()
    unwrapper.sweepETH({"from":ychad})
    assert ychad.balance() == ychad_before + eth_bal
    assert unwrapper.balance() == 0

def test_sweep_erc20(unwrapper, ychad, chain, rando, weth):
    weth.transfer(unwrapper, 1e18, {"from":ychad})
    weth_bal = weth.balanceOf(unwrapper)
    assert weth_bal > 0
    amt = weth.balanceOf(ychad)
    weth.approve(unwrapper, 2**256-1, {"from":ychad})
    ychad_before = ychad.balance()
    ychad_weth_before = weth.balanceOf(ychad)
    unwrapper.unwrap(amt,{"from":ychad})
    assert ychad_before + amt == ychad.balance()
    assert weth_bal == weth.balanceOf(unwrapper) # Make sure user got exactly amount they requested
    ychad_before = ychad.balance()
    unwrapper.sweepToken(weth,{"from":ychad})
    assert weth.balanceOf(unwrapper) == 0
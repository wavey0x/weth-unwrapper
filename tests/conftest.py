import pytest, web3
from brownie import config, Contract, accounts, interface
from brownie import network

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

@pytest.fixture
def ychad(accounts, web3):
    yield accounts.at(web3.ens.resolve("ychad.eth"), force=True)

@pytest.fixture
def rando(accounts):
    yield accounts[0]

@pytest.fixture
def rando(accounts):
    yield accounts[0]

@pytest.fixture
def unwrapper(Unwrapper, rando):
    # unwrapper = Contract("0xDf270b48829E0F05211F3A33E5Dc0A84F7247FBE")
    unwrapper = rando.deploy(Unwrapper)
    yield unwrapper

@pytest.fixture
def weth():
    yield Contract("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
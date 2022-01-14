pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";
import "@openzeppelin/contracts/math/Math.sol";

interface IWeth {
    function withdraw(uint wad) external;
    function transferFrom(address src, address dst, uint wad) external returns (bool);
}

contract Unwrapper {
    using SafeERC20 for IERC20;
    using Address for address;

    address public governance;
    IWeth public weth;

    constructor() public {
        governance = 0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52;
        weth = IWeth(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2);
    }

    function unwrap(uint256 _amount) external {
        require(_amount > 0, "!Zero");
        weth.transferFrom(msg.sender, address(this), _amount);
        weth.withdraw(_amount);
        (bool success, bytes memory data) = msg.sender.call{value: _amount}("");
        require(success, "!Send");
    }

    function sweepToken(address _token) external {
        require(msg.sender == governance, "!authorized");
        IERC20(_token).safeTransfer(address(governance), IERC20(_token).balanceOf(address(this)));
    }

    function sweepETH() external {
        require(msg.sender == governance, "!authorized");
        (bool success, bytes memory returnData) = governance.call{value: address(this).balance}("");
        require(success, "!Sweep");
    }

    receive() external payable {}
}

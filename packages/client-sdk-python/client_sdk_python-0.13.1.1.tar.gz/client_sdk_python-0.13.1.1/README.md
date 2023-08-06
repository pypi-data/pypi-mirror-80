# client-sdk-python

[![Join the chat at https://gitter.im/ethereum/web3.py](https://badges.gitter.im/ethereum/web3.py.svg)](https://github.com/PlatONnetwork/client-sdk-python)

[![Build Status](https://circleci.com/gh/ethereum/web3.py.svg?style=shield)](https://github.com/PlatONnetwork/client-sdk-python)


A Python implementation of [web3.js](https://github.com/ethereum/web3.js)

* Python 3.6+ support

Read more in the [documentation on ReadTheDocs](http://web3py.readthedocs.io/). [View the change log on Github](docs/releases.rst).

## Quickstart

```python


from client_sdk_python import Web3, HTTPProvider
from client_sdk_python.eth import PlatON
from hexbytes import HexBytes

# get blockNumber
w3 = Web3(HTTPProvider("http://localhost:6789"))
platon = PlatON(w3)
block_number = platon.blockNumber
print(block_number)

# get Balance
address = '0x493301712671Ada506ba6Ca7891F436D29185821'
balance = platon.getBalance(address)
print(balance)

# sendtransaction
to = '0xC1f330B214668beAc2E6418Dd651B09C759a4Bf5'
w3.personal.unlockAccount(address, "password", 60)
data = {
    "from": address,
    "to": to,
    "value": 0x10909,
}
transaction_hex = HexBytes(platon.sendTransaction(data)).hex()
result = platon.waitForTransactionReceipt(transaction_hex)
print(result)
```

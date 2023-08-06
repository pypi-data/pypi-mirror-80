# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cosmospy']

package_data = \
{'': ['*']}

install_requires = \
['bech32>=1.1.0,<2.0.0',
 'ecdsa>=0.14.0,<0.17.0',
 'hdwallets>=0.1.0,<0.2.0',
 'mnemonic>=0.19,<0.20']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'cosmospy',
    'version': '5.1.0',
    'description': 'Tools for Cosmos wallet management and offline transaction signing',
    'long_description': '[![Build Status](https://travis-ci.com/hukkinj1/cosmospy.svg?branch=master)](<https://travis-ci.com/hukkinj1/cosmospy>)\n[![codecov.io](https://codecov.io/gh/hukkinj1/cosmospy/branch/master/graph/badge.svg)](<https://codecov.io/gh/hukkinj1/cosmospy>)\n[![PyPI version](https://badge.fury.io/py/cosmospy.svg)](<https://badge.fury.io/py/cosmospy>)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](<https://github.com/psf/black>)\n\n# cosmospy\n\n<!--- Don\'t edit the version line below manually. Let bump2version do it for you. -->\n\n> Version 5.1.0\n\n> Tools for Cosmos wallet management and offline transaction signing\n\n## Installing\n\nInstalling from PyPI repository (https://pypi.org/project/cosmospy):\n\n~~~bash\npip install cosmospy\n~~~\n\n## Usage\n\n### Generating a wallet\n\n~~~python\nfrom cosmospy import generate_wallet\n\nwallet = generate_wallet()\n~~~\n\nThe value assigned to `wallet` will be a dictionary just like:\n\n~~~python\n{\n    "seed": "arch skill acquire abuse frown reject front second album pizza hill slogan guess random wonder benefit industry custom green ill moral daring glow elevator",\n    "derivation_path": "m/44\'/118\'/0\'/0/0",\n    "private_key": b"\\xbb\\xec^\\xf6\\xdcg\\xe6\\xb5\\x89\\xed\\x8cG\\x05\\x03\\xdf0:\\xc9\\x8b \\x85\\x8a\\x14\\x12\\xd7\\xa6a\\x01\\xcd\\xf8\\x88\\x93",\n    "public_key": b"\\x03h\\x1d\\xae\\xa7\\x9eO\\x8e\\xc5\\xff\\xa3sAw\\xe6\\xdd\\xc9\\xb8b\\x06\\x0eo\\xc5a%z\\xe3\\xff\\x1e\\xd2\\x8e5\\xe7",\n    "address": "cosmos1uuhna3psjqfxnw4msrfzsr0g08yuyfxeht0qfh",\n}\n~~~\n\n### Converter functions\n\n#### Mnemonic seed to private key\n\n~~~python\nfrom cosmospy import BIP32DerivationError, seed_to_privkey\n\nseed = (\n    "teach there dream chase fatigue abandon lava super senior artefact close upgrade"\n)\ntry:\n    privkey = seed_to_privkey(seed, path="m/44\'/118\'/0\'/0/0")\nexcept BIP32DerivationError:\n    print("No valid private key in this derivation path!")\n~~~\n\n#### Private key to public key\n\n~~~python\nfrom cosmospy import privkey_to_pubkey\n\nprivkey = bytes.fromhex(\n    "6dcd05d7ac71e09d3cf7da666709ebd59362486ff9e99db0e8bc663570515afa"\n)\npubkey = privkey_to_pubkey(privkey)\n~~~\n\n#### Public key to address\n\n~~~python\nfrom cosmospy import pubkey_to_address\n\npubkey = bytes.fromhex(\n    "03e8005aad74da5a053602f86e3151d4f3214937863a11299c960c28d3609c4775"\n)\naddr = pubkey_to_address(pubkey)\n~~~\n\n#### Private key to address\n\n~~~python\nfrom cosmospy import privkey_to_address\n\nprivkey = bytes.fromhex(\n    "6dcd05d7ac71e09d3cf7da666709ebd59362486ff9e99db0e8bc663570515afa"\n)\naddr = privkey_to_address(privkey)\n~~~\n\n### Signing transactions\n\n~~~python\nfrom cosmospy import Transaction\n\ntx = Transaction(\n    privkey=bytes.fromhex(\n        "26d167d549a4b2b66f766b0d3f2bdbe1cd92708818c338ff453abde316a2bd59"\n    ),\n    account_num=11335,\n    sequence=0,\n    fee=1000,\n    gas=70000,\n    memo="",\n    chain_id="cosmoshub-3",\n    sync_mode="sync",\n)\ntx.add_transfer(\n    recipient="cosmos103l758ps7403sd9c0y8j6hrfw4xyl70j4mmwkf", amount=387000\n)\ntx.add_transfer(recipient="cosmos1lzumfk6xvwf9k9rk72mqtztv867xyem393um48", amount=123)\npushable_tx = tx.get_pushable()\n~~~\n\nOne or more token transfers can be added to a transaction by calling the `add_transfer` method.\n\nWhen the transaction is fully prepared, calling `get_pushable` will return a signed transaction in the form of a JSON string.\nThis can be used as request body when calling the `POST /txs` endpoint of the [Cosmos REST API](<https://cosmos.network/rpc>).\n',
    'author': 'hukkinj1',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hukkinj1/cosmospy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

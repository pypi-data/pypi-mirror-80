# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiger_discrete']

package_data = \
{'': ['*']}

install_requires = \
['funcy>=1.14,<2.0',
 'py-aiger-bv>=4.3.0,<5.0.0',
 'py-aiger-ptltl>=3.0.1,<4.0.0',
 'pyrsistent>=0.17.3,<0.18.0']

setup_kwargs = {
    'name': 'py-aiger-discrete',
    'version': '0.1.1',
    'description': 'Library for modeling functions over discrete sets using aiger circuits.',
    'long_description': "# py-aiger-discrete\nLibrary for modeling functions over discrete sets using aiger circuits.\n\n[![Build Status](https://cloud.drone.io/api/badges/mvcisback/py-aiger-discrete/status.svg)](https://cloud.drone.io/mvcisback/py-aiger-discrete)\n[![docs badge](https://img.shields.io/badge/docs-docs-black)](https://mjvc.me/py-aiger-discrete)\n[![codecov](https://codecov.io/gh/mvcisback/py-aiger-discrete/branch/main/graph/badge.svg)](https://codecov.io/gh/mvcisback/py-aiger-discrete)\n[![PyPI version](https://badge.fury.io/py/py-aiger_discrete.svg)](https://badge.fury.io/py/py-aiger-discrete)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n# Installation\n\nIf you just need to use `py-aiger-discrete`, you can just run:\n\n`$ pip install py-aiger-discrete`\n\nFor developers, note that this project uses the\n[poetry](https://poetry.eustace.io/) python package/dependency\nmanagement tool. Please familarize yourself with it and then\nrun:\n\n`$ poetry install`\n\n   \n# About\n\nThis library helps with modeling functions over finite sets using circuits. \n\n    f : A → B₁ × B₂ × … × Bₘ\n\nwhere `A ⊆ A₁ × A₂ × … × Aₙ`.\n\nThis is done by providing:\n\n1. A encoder/decoder pair for each set to and from (unsigned)\n   integers. \n2. A circuit that uses the bit-vector representation of these integers\n   to compute `f`.\n3. A circuit that monitors if the input bit-vector sequence is\n   `valid`, i.e., a member of `A`.\n\nFunctionally, the `py-aiger-discrete` library centers around the\n`aiger_discrete.FiniteFunc` class which has 4 attributes an `aiger_bv.AIGBV` object.\n\n1. A string `valid_id` indicating\n1. A circuit, `circ`, over named bit-vectors in the form of an\n   `aiger_bv.AIGBV` object. One of the outputs must be named\n   `valid_id`.\n1. A mapping from **inputs** to `aiger_discrete.Encoding` objects which\n   encode/decode objects to integers. The standard bit-encoding of\n   unsigned integers is feed into `circ`.\n1. A mapping from **outputs** to `aiger_discrete.Encoding` objects which\n   encode/decode objects to integers. These encodings are used to decode\n   the resulting bit-vectors of `circ`.\n\n# Usage\n\nBelow we provide a basic usage example. This example assumes basic\nknowledge of the `py-aiger` ecosystem and particularly `py-aiger-bv`.\n\n```python\nimport aiger_bv as BV\n\nfrom aiger_discrete import Encoding, from_aigbv\n\n# Will assume inputs are in 'A', 'B', 'C', 'D', or 'E'.\nascii_encoder = Encoding(\n    decode=lambda x: chr(x + ord('A')),  # Make 'A' map to 0.\n    encode=lambda x: ord(x) - ord('A'),\n)\n\n# Create function which maps: A -> B, B -> C, C -> D, D -> E.\n\nx = BV.uatom(3, 'x')  # need 3 bits to capture 5 input types.\nupdate_expr = (x + 1) & 0b111\ncirc = update_expr.with_output('y').aigbv\n\n# Need to assert that the inputs are less than 4.\ncirc |= (x <= 4).with_output('##valid').aigbv\n\nfunc = from_aigbv(\n    circ,\n    input_encodings={'x': ascii_encoder},\n    output_encodings={'y': ascii_encoder},\n    valid_id='##valid',\n)\n\nassert func('A') == 'B'\nassert func('B') == 'C'\nassert func('C') == 'D'\nassert func('D') == 'E'\nassert func('E') == 'A'\n```\n\nNote that `py-aiger-discrete` implements most of the circuit API as `aiger_bv.AIGBV`. \n\nFor example, sequential composition:\n\n```python\nfunc12 = func1 >> func2\n```\n\nor parallel composition:\n\n```python\nfunc12 = func1 | func2\n```\n\nor unrolling:\n\n```python\nfunc_unrolled = func1.unroll(5)\n```\n\nor feedback:\n\n```python\nfunc_cycle = func1.loopback({\n    'input': 'x',\n    'output': 'y',\n    'keep_output': True,\n})\n```\n\nor renaming:\n```python\nfunc_renamed = func1['i', {'x': 'z'}]\nassert func1.inputs == {'z'}\n```\n",
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mvcisback/py-aiger-discrete',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

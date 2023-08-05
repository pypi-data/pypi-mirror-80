# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ina260']

package_data = \
{'': ['*']}

install_requires = \
['smbus2>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'ina260',
    'version': '0.0.2',
    'description': 'A generic Python library for the INA260 power monitor chip',
    'long_description': "# INA260 Driver\n\n![coverage](coverage.svg)\n\n## Introduction\n\nThis Python package provides a platform agnostic driver for the [TI INA260](https://www.ti.com/product/INA260) precision power monitor. Conveniently, the INA260 has a built-in sense resistor so it's very easy to integrate into your projects. It can sense from 0 to 36V and up to 15A(!) with 16-bit resolution. Thus, it's perfect for pretty much all hobbyist projects.\n\nThe only dependency for this library is `smbus2` so provided your I2C device is addressable by that, this library should work (for example on a Raspberry Pi or other dev board).\n\n## Examples\n\n```python\n\nfrom ina260.controller import Controller\n\nc = Controller(address=0x40)\n\nprint(c.voltage())\nprint(c.current())\nprint(c.power()))\n\n```\n\nsee the example script in the repository. Note that the power measurement is usually not the same as voltage times current unless you read all three registers instantaneously.\n\nObviously check what address you've set the chip to (there is a table in the datasheet).\n\n## Hardware notes\n\nThe chip itself is very easy to hook up (although it comes in a VSSOP package which can be challenging to solder if you've not had much experience with SMD soldering).\n\nBe sure to follow TI's guidelines in the datasheet about proper power planes and PCB layout. The package is designed so that your power rail goes in one side and out the other. Otherwise the chip is very easy to integrate and minimally just needs a standard 0.1uF bypass capacitor.\n\n## Test suite\n\nThis package has a comprehensive test suite which you can use to check that commands are being recieved and interpreted properly. You need `pytest`. Run with:\n\n```\npython -m pytest test\n```\n\nCoverage is 99% because there should also be a check for reverse current which is obviously difficult to do simultaneously with forward current.\n\n",
    'author': 'Josh Veitch-Michaelis',
    'author_email': 'j.veitchmichaelis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jveitchmichaelis/ina260',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)

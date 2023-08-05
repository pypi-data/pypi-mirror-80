# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dicetray']

package_data = \
{'': ['*']}

install_requires = \
['sly>=0.4,<0.5']

setup_kwargs = {
    'name': 'dicetray',
    'version': '1.0.0',
    'description': 'Tabletop RPG Dice roller',
    'long_description': "Dicetray\n========\n\n.. image:: https://github.com/gtmanfred/dicetray/workflows/Tests/badge.svg\n    :target: https://github.com/gtmanfred/dicetray\n\n.. image:: https://img.shields.io/codecov/c/github/gtmanfred/dicetray\n    :target: https://codecov.io/gh/gtmanfred/dicetray\n\n.. image:: https://img.shields.io/pypi/v/dicetray\n    :target: https://pypi.org/project/dicetray\n\n.. image:: https://img.shields.io/pypi/l/dicetray\n    :target: http://www.apache.org/licenses/LICENSE-2.0\n\n.. image:: https://img.shields.io/pypi/dm/dicetray\n    :target: https://pypi.org/project/dicetray/\n\n\nTabletop RPG Dice rolling manager.\n\nThis library uses system random generator in order to have truely random dice rolls.\n\nExample\n-------\n\n.. code-block:: python\n\n    >>> from dicetray import Dicetray\n    >>> Dicetray('1d20 + 3').roll()\n    15\n    >>> Dicetray('4d6dl').roll()\n    10\n    >>> Dicetray('4d6kh3').roll()\n    12\n    >>> d = Dicetray('2d20kh + 1d4 + 3')\n    >>> d.result\n    >>> d.dice\n    set()\n    >>> d.roll()\n    18\n    >>> d.dice\n    {<Dice (d20): 14>, <Dice (d20): 14>, <Dice (d4): 1>}\n    >>> d.result\n    18\n",
    'author': 'Daniel Wallace',
    'author_email': 'danielwallace@gtmanfred.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gtmanfred/dicetray.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

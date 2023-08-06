# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sportorg',
 'sportorg.common',
 'sportorg.gui',
 'sportorg.gui.dialogs',
 'sportorg.gui.menu',
 'sportorg.gui.tabs',
 'sportorg.gui.utils',
 'sportorg.libs',
 'sportorg.libs.iof',
 'sportorg.libs.ocad',
 'sportorg.libs.sfr',
 'sportorg.libs.sportiduino',
 'sportorg.libs.telegram',
 'sportorg.libs.template',
 'sportorg.libs.winorient',
 'sportorg.models',
 'sportorg.models.result',
 'sportorg.models.start',
 'sportorg.modules',
 'sportorg.modules.backup',
 'sportorg.modules.configs',
 'sportorg.modules.iof',
 'sportorg.modules.live',
 'sportorg.modules.ocad',
 'sportorg.modules.printing',
 'sportorg.modules.sfr',
 'sportorg.modules.sound',
 'sportorg.modules.sportident',
 'sportorg.modules.sportiduino',
 'sportorg.modules.telegram',
 'sportorg.modules.updater',
 'sportorg.modules.winorient',
 'sportorg.utils']

package_data = \
{'': ['*'], 'sportorg.libs.iof': ['data/*']}

install_requires = \
['PySide2>=5,<6',
 'boltons>=20,<21',
 'docxtpl>=0,<1',
 'jinja2>=2,<3',
 'playsound>=1,<2',
 'polib>=1,<2',
 'pydantic>=1,<2',
 'python-dateutil>=2,<3',
 'python-dotenv>=0.14,<0.15',
 'pywinusb>=0,<1',
 'requests>=2,<3',
 'shiboken2>=5.15,<6.0',
 'sportident>=1,<2']

extras_require = \
{'win': ['pywin32>=228,<229']}

setup_kwargs = {
    'name': 'sportorg',
    'version': '1.4.0',
    'description': 'SportOrg, python, sportident, orienteering',
    'long_description': None,
    'author': 'Danil Akhtarov',
    'author_email': 'daxartio@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)

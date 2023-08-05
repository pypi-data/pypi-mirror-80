# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xplainet']

package_data = \
{'': ['*']}

install_requires = \
['scikit-learn>=0.21,<1.0.0',
 'tensorflow-addons==0.11.2',
 'tensorflow>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'xplainet',
    'version': '0.1.0',
    'description': 'Explainable Neural network in Keras',
    'long_description': '# XplaiNet\n',
    'author': 'Hartorn',
    'author_email': 'hartorn.github@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Hartorn/XplaiNet',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

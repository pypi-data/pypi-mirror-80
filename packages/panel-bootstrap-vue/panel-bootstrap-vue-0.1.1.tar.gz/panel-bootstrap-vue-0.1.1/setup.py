# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['panel_bootstrap_vue', 'panel_bootstrap_vue.www.typography.fonts']

package_data = \
{'': ['*'],
 'panel_bootstrap_vue': ['www/bootstrap/*',
                         'www/typography/*',
                         'www/typography/fonts/adobe-source-sans-pro/*',
                         'www/typography/fonts/font-awesome/*',
                         'www/vue/*']}

install_requires = \
['panel-components>=0.1.0,<0.2.0', 'panel>=0.9.7,<0.10.0']

setup_kwargs = {
    'name': 'panel-bootstrap-vue',
    'version': '0.1.1',
    'description': 'Use bootstrap-vue VueJs components supporting Bootstrap 4 in Panel templates.',
    'long_description': None,
    'author': 'Paulo Lopes',
    'author_email': 'paulopes00@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

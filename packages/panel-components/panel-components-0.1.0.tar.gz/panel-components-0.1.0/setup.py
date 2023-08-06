# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['panel_components', 'panel_components.www.katex.fonts']

package_data = \
{'': ['*'],
 'panel_components': ['www/ace/*',
                      'www/bokeh/*',
                      'www/katex/*',
                      'www/mathjax/*',
                      'www/plotly/*',
                      'www/vega/*',
                      'www/vtk/*',
                      'www/vue/*']}

install_requires = \
['panel>=0.9.7,<0.10.0']

setup_kwargs = {
    'name': 'panel-components',
    'version': '0.1.0',
    'description': 'HTML components for Panel templates.',
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

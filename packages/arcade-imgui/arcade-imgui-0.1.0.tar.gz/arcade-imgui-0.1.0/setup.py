# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcade_imgui']

package_data = \
{'': ['*']}

install_requires = \
['PyOpenGL>=3.0.0,<4.0.0', 'arcade>=2.4.2,<3.0.0', 'imgui>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'arcade-imgui',
    'version': '0.1.0',
    'description': 'IMGUI integration for arcade',
    'long_description': '# Arcade ImGui\n\n[The Python Arcade Library](https://arcade.academy/) + [pyimgui](https://github.com/swistakm/pyimgui) = :heart:\n\n## Install\n\nClone the repository\n\n        pip install git+https://github.com/kfields/arcade-imgui.git\n        \n\n## Run\n\nFull Demo\n\n        python example_arcade.py\n\nNumber Input Test\n\n        python example_arcade_input.py\n',
    'author': 'Kurtis Fields',
    'author_email': 'kurtisfields@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kfields/arcade-imgui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

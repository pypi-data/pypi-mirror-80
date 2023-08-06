# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['akun_tools']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'click>=7.1.2,<8.0.0',
 'html5lib>=1.1,<2.0',
 'python-magic>=0.4.18,<0.5.0',
 'qtoml>=0.3.0,<0.4.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['akun_scraper = akun_tools.scraper:scraper']}

setup_kwargs = {
    'name': 'akun-tools',
    'version': '0.1.0',
    'description': 'Tools for interacting with anonkun/fiction.live',
    'long_description': 'akun-tools\n==========\n\nakun-tools is a set of tools for interacting with Fiction.live, previously known\nas anonkun. Currently it includes a scraper that generates HTML ebooks of quests.\n\nakun-tools is a command-line utility that requires Python 3 and pip. To install\nit, run:\n\n.. code:: bash\n\n  $ pip install akun-tools\n\nOnce installed, you run it with ``akun_scraper``. Example usage:\n\n.. code:: bash\n\n  $ akun_scraper getinfo https://fiction.live/stories/Abyssal-Admiral-Quest-/QGSpwAtjf9NMtvsTA/home\n  $ akun_scraper download abyssal_admiral_quest.toml\n',
    'author': 'alethiophile',
    'author_email': 'alethiophile.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alethiophile/qtoml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

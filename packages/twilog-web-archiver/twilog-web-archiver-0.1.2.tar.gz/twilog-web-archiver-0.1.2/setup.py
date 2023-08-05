# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twilog_web_archiver']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'click>=7.0,<8.0',
 'lxml>=4.3,<5.0',
 'pluggy>=0.13.1,<0.14.0',
 'requests>=2.21,<3.0',
 'savepagenow>=0.0.12,<1.1.1']

entry_points = \
{'console_scripts': ['twilog-web-archiver = twilog_web_archiver.main:main']}

setup_kwargs = {
    'name': 'twilog-web-archiver',
    'version': '0.1.2',
    'description': 'Save month list pages of twilog.org by using archive.org.',
    'long_description': 'twilog-web-archiver\n===================\n\n.. image:: https://circleci.com/gh/shuuji3/twilog-web-archiver.svg?style=svg\n    :target: https://circleci.com/gh/shuuji3/twilog-web-archiver\n\nSave month list pages of twilog.org using archive.org.\n\nRequirement\n-----------\n\n- :code:`Python >= 3.6`\n\nInstall\n-------\n\n.. code-block:: bash\n\n    $ pip install twilog-web-archiver\n\nUsage\n-----\n\n.. code-block:: bash\n\n    $ twilog-web-archiver SCREEN_NAME\n\nDescription\n-----------\n\nWhen a user has registered twilog.org, you will see the month list page in the user archive page, i.e. `https://twilog.org/NHK_PR/archives <https://twilog.org/NHK_PR/archives>`_.\n\nThis program saves every pages in this month list into Wayback Machine on `archive.org <archive.org>`_.\n\nLicense\n-------\n\n- `GNU GPL 3.0 or later <LICENSE>`_\n',
    'author': 'TAKAHASHI Shuuji',
    'author_email': 'shuuji3@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shuuji3/twilog-web-archiver',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

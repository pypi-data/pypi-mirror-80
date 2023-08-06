# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['votion', 'votion.tests']

package_data = \
{'': ['*']}

install_requires = \
['docker>=4.2.0,<5.0.0']

entry_points = \
{'console_scripts': ['votion = votion.main:main']}

setup_kwargs = {
    'name': 'votion',
    'version': '0.0.5',
    'description': 'Docker image build tool',
    'long_description': "# votion\n\n[![Build Status](https://travis-ci.org/weastur/votion.svg?branch=master)](https://travis-ci.org/weastur/votion)\n[![codecov](https://codecov.io/gh/weastur/votion/branch/master/graph/badge.svg)](https://codecov.io/gh/weastur/votion)\n[![Documentation Status](https://readthedocs.org/projects/votion/badge/?version=latest)](https://votion.readthedocs.io/en/latest/?badge=latest)\n[![PyPi version](https://img.shields.io/pypi/v/votion.svg)](https://pypi.org/project/votion/)\n[![Python versions](https://img.shields.io/pypi/pyversions/votion)](https://pypi.org/project/votion/)\n[![black-formatter](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/) [![Join the chat at https://gitter.im/votion-build-tool/community](https://badges.gitter.im/votion-build-tool/community.svg)](https://gitter.im/votion-build-tool/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n\n---\n\nDocker image build tool\n\n## Features\n\n## Documentation\n\nFor full documentation please go [here](https://votion.readthedocs.io/en/latest/).\n\n## Instalation\n\n```bash\npip install votion\n```\n\n## Development\n\nFor development first you need [poetry](https://github.com/python-poetry/poetry) and python 3.7+\n\n```bash\ngit clone git@github.com:weastur/votion.git\ncd votion\npoetry install\n```\n\nThis will install dependencies and all needed packages for development, like pytest, wemake-python-styleguide, mypy, black.\n\nHighly recommend to install [overcommit](https://github.com/sds/overcommit).\n\n```bash\novercommit -i\n```\n\nAfter, all commits will be checked on set of rules when you create them. Additionally\non CI executed flake8, mypy, black, and unit tests. You can easily integrate same checks into your editor.\nThis checks aren't executed with hooks, because otherwise you'll be able to commit only inside virtualenv.\n\n## Bugs/Requests\n\n## Changelog\n\n## Roadmap\n\n## License\n\nDistributed under the terms of the [MIT](https://github.com/weastur/votion/blob/master/LICENSE) license, pytest is free and open source software.\n",
    'author': 'Pavel Sapezhko',
    'author_email': 'me@weastur.com',
    'maintainer': 'Pavel Sapezhko',
    'maintainer_email': 'me@weastur.com',
    'url': 'https://github.com/weastur/votion',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

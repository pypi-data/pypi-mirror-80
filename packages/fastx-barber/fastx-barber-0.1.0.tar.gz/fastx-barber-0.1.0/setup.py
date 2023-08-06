# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastx_barber', 'fastx_barber.scripts']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.77,<2.0',
 'joblib>=0.16.0,<0.17.0',
 'numpy>=1.19.1,<2.0.0',
 'pandas>=1.1.2,<2.0.0',
 'regex>=2020.7.14,<2021.0.0',
 'rich>=7.1.0,<8.0.0',
 'tqdm>=4.48.1,<5.0.0']

entry_points = \
{'console_scripts': ['fbarber = fastx_barber.scripts.barber:main']}

setup_kwargs = {
    'name': 'fastx-barber',
    'version': '0.1.0',
    'description': 'FASTX trimming tools',
    'long_description': "# fastx-barber\n\n[![DOI](https://zenodo.org/badge/281703558.svg)](https://zenodo.org/badge/latestdoi/281703558) ![](https://img.shields.io/librariesio/github/ggirelli/fastx-barber.svg?style=flat) ![](https://img.shields.io/github/license/ggirelli/fastx-barber.svg?style=flat)  \n![](https://github.com/ggirelli/fastx-barber/workflows/Python%20package/badge.svg?branch=master&event=push) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastx-barber) ![PyPI - Format](https://img.shields.io/pypi/format/fastx-barber) ![PyPI - Status](https://img.shields.io/pypi/status/fastx-barber)  \n![](https://img.shields.io/github/release/ggirelli/fastx-barber.svg?style=flat) ![](https://img.shields.io/github/release-date/ggirelli/fastx-barber.svg?style=flat) ![](https://img.shields.io/github/languages/code-size/ggirelli/fastx-barber.svg?style=flat)  \n![](https://img.shields.io/github/watchers/ggirelli/fastx-barber.svg?label=Watch&style=social) ![](https://img.shields.io/github/stars/ggirelli/fastx-barber.svg?style=social)\n\n[PyPi](https://pypi.org/project/fastx-barber/) | [docs](https://ggirelli.github.io/fastx-barber/)\n\nA Python3.6.1+ package to trim and extract flags from FASTA  and FASTQ files.\n\n## Features (in short)\n\n* Works on both FASTA and FASTQ files.\n* Selects reads based on a pattern (regex).\n* Trims reads by pattern (regex), length, or single-base quality.\n* Extracts parts (flags) of reads based on a pattern and stores them in the read headers.\n* Regular expression support [*fuzzy* matching](https://pypi.org/project/regex/#approximate-fuzzy-matching-hg-issue-12-hg-issue-41-hg-issue-109) (*fuzzy matching* might affect the barber's speed).\n* Parallelizes processing by splitting the fastx file in chunks.\n\nFor more available features, check out our [docs](https://ggirelli.github.io/fastx-barber/)!\n\n## Requirements\n\n`fastx-barber` has been tested with Python 3.6.1, 3.7, and 3.8. We recommend installing it using `pipx` (see [below](https://github.com/ggirelli/fastx-barber#install)) to avoid dependency conflicts with other packages. The packages it depends on are listed in our [dependency graph](https://github.com/ggirelli/fastx-barber/network/dependencies). We use [`poetry`](https://github.com/python-poetry/poetry) to handle our dependencies.\n\n## Install\n\nWe recommend installing `fastx-barber` using [`pipx`](https://github.com/pipxproject/pipx). Check how to install `pipx` [here](https://github.com/pipxproject/pipx#install-pipx) if you don't have it yet!\n\nOnce you have `pipx` ready on your system, install the latest stable release of `fastx-barber` by running: `pipx install fastx-barber`. If you see the stars (✨ 🌟 ✨), then the installation went well!\n\n## Usage\n\nRun:\n\n* `fbarber` to access the barber's services.\n* `fbarber flag` to extract or manipulate read flags.\n* `fbarber match` to select reads based on a pattern (regular expression).\n* `fbarber trim` to trim your reads.\n\nAdd `-h` to see the full help page of a command!\n\n## Contributing\n\nWe welcome any contributions to `fastx-barber`. In short, we use [`black`](https://github.com/psf/black) to standardize code format. Any code change also needs to pass `mypy` checks. For more details, please refer to our [contribution guidelines](https://github.com/ggirelli/fastx-barber/blob/master/CONTRIBUTING.md) if this is your first time contributing! Also, check out our [code of conduct](https://github.com/ggirelli/fastx-barber/blob/master/CODE_OF_CONDUCT.md).\n\n## License\n\n`MIT License - Copyright (c) 2020 Gabriele Girelli`\n",
    'author': 'Gabriele Girelli',
    'author_email': 'gigi.ga90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ggirelli/fastx-barber',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

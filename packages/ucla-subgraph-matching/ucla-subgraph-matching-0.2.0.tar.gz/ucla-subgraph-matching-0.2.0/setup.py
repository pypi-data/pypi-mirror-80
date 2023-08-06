# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uclasm', 'uclasm.counting', 'uclasm.filters', 'uclasm.utils']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.4,<3.0',
 'numpy>=1.18.1,<2.0.0',
 'pandas>=1.0.1,<2.0.0',
 'scipy>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'ucla-subgraph-matching',
    'version': '0.2.0',
    'description': '',
    'long_description': '<div align="center">\n<img src="logo.png" alt="logo">\n</div>\n\n<h2 align="center">Subgraph Matching on Multiplex Networks</h2>\n\n<div align="center">\n<a href="https://zenodo.org/badge/latestdoi/148378128"><img alt="Zenodo Archive" src="https://zenodo.org/badge/148378128.svg"></a>\n<a href="https://pypi.org/project/ucla-subgraph-matching/"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/ucla-subgraph-matching.svg"></a>\n<a href="https://pypi.org/project/ucla-subgraph-matching/"><img alt="Supported Python Versions" src="https://img.shields.io/pypi/pyversions/ucla-subgraph-matching.svg"></a>\n</div>\n\nTo reproduce our experiments, you will need at least Python 3.7 and a few packages installed. You can check your python version with\n\n```bash\n$ python --version\n```\nand install the necessary packages with\n```bash\n$ python -m pip install numpy scipy pandas tqdm matplotlib networkx\n```\n\nYou will also need a local copy of our code either cloned from GitHub or downloaded from a Zenodo archive. To install our package from your local copy of the code, change to the code directory and use pip.\n\n```bash\n$ cd ucla-subgraph-matching\n$ python -m pip install .\n```\n\n### Erdős–Rényi Experiments\n\nRunning the experiments will take a while depending on your hardware.\n\n```bash\n$ cd experiments\n$ python run_erdos_renyi.py\n$ python plot_erdos_renyi.py\n```\nChange the variables in run_erdos_renyi.py to run with different settings i.e. number of layers and whether isomorphism counting is being done.\n\nplot_erdos_renyi.py will generate a figure called `n_iter_vs_n_world_nodes_3_layers_500_trials_iso_count.pdf` which corresponds to figure 7 in the paper. Other figures related to time and number of isomorphisms will also be generated.\n\n### Sudoku Experiments\n\nRunning the experiments will take a while depending on your hardware.\n\n```bash\n$ cd experiments\n$ python run_sudoku.py\n$ python plot_sudoku_times.py\n```\n\nplot_sudoku_times.py will generate a figure called `test_sudoku_scatter_all_log.pdf` which corresponds to figure 6 in the paper. Other figures for each individual dataset will also be generated.\n',
    'author': 'Jacob Moorman',
    'author_email': 'jacob@moorman.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jdmoorman/uclasm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

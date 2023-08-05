# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nxv', 'nxv.html_like', 'nxv.styles']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5,<3.0']

setup_kwargs = {
    'name': 'nxv',
    'version': '0.1.0',
    'description': 'Render NetworkX graphs using GraphViz',
    'long_description': '<img src="./docs/_static/logo/logo.svg" align="left">\n\n# nxv\n\nRender NetworkX graphs using GraphViz.\n\n# Documentation\n\nhttps://nxv.readthedocs.io/\n\n# Basic Usage\n\n    import networkx as nx\n    import nxv\n    \n    graph = nx.Graph()\n    graph.add_edge("A", "B")\n    graph.add_edge("B", "C")\n    graph.add_edge("C", "D")\n    graph.add_edge("B", "E")\n\n    style = nxv.Style(\n        graph={"rankdir": "LR"},\n        node=lambda u, d: {"shape": "circle" if u in "AEIOU" else "square"},\n        edge=lambda u, v, d: {"style": "dashed", "label": u + v},\n    )\n    \n    nxv.render(graph, style)\n\n<img src="./docs/_static/example/quickstart_graph_functional_style.svg">\n\n# Installation\n\n    pip install nxv\n\n# Development\n\nThis repository uses\n[Poetry](https://python-poetry.org/) and\n[Nox](https://nox.thea.codes/en/stable/)\nto manage the development environment and builds.\n\nTo list all Nox sessions:\n\n    python -m nox --list-sessions\n\nTo run the black code formatter:\n\n    python -m nox -rs black\n\nTo lint using flake8:\n\n    python -m nox -rs lint\n\nTo run the test suite:\n\n    python -m nox -rs tests\n\nTo build the documentation:\n\n    python -m nox -rs docs\n',
    'author': 'Timothy Shields',
    'author_email': 'Timothy.Shields@twosigma.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/twosigma/nxv',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

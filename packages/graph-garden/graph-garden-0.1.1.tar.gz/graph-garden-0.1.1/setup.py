# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graph_garden']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'beautifulsoup4>=4.9.1,<5.0.0',
 'circus>=0.17.1,<0.18.0',
 'psutil>=5.7.2,<6.0.0',
 'pySmartDL>=1.3.3,<2.0.0',
 'python-arango>=6.0.0,<7.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['graph-garden = graph_garden.cli:app']}

setup_kwargs = {
    'name': 'graph-garden',
    'version': '0.1.1',
    'description': 'Python library for managing ArangoDB instance',
    'long_description': '# Graph Garden\nPython library for managing ArangoDB instance\n\n[ArangoDB](https://www.arangodb.com/) is a trademark and property of ArangoDB, Inc. Graph Garden library is just a convenient way of managing ArangoDB instance from CLI and Python code (setup, start, stop). It is not developed or endorsed by ArangoDB, Inc.\n\n## Installation\n\n```bash\npip install graph-garden\n```\n\n## Usage\n\nRun the following command to get help:\n\n```bash\ngraph-garden --help\n```\n\nYou can also see how Graph Garden is currently used in [ConceptNet Rocks!](https://github.com/ldtoolkit/conceptnet-rocks).\n',
    'author': 'Roman Inflianskas',
    'author_email': 'infroma@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ldtoolkit/graph-garden',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

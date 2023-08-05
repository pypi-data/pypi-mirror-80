# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conceptnet_rocks', 'conceptnet_rocks.conceptnet5']

package_data = \
{'': ['*']}

install_requires = \
['dask[dataframe]>=2.27.0,<3.0.0',
 'graph-garden>=0.1.2,<0.2.0',
 'orjson>=3.3.1,<4.0.0',
 'python-arango>=6.0.0,<7.0.0',
 'tqdm>=4.48.2,<5.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['conceptnet-rocks-load = conceptnet_rocks.cli:app']}

setup_kwargs = {
    'name': 'conceptnet-rocks',
    'version': '0.1.2',
    'description': 'Python library to work with ConceptNet offline',
    'long_description': '# ConceptNet Rocks!\n\nWork is in progress.\n\nThe library comes with Apache License 2.0, and is separate from ConceptNet itself, although it uses some parts of its code. The ConceptNet is available under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) license. See [here](https://github.com/commonsense/conceptnet5/wiki/Copying-and-sharing-ConceptNet) for the list of conditions for using ConceptNet data.\n\nThis is the official citation for ConceptNet if you use it in research:\n\n> Robyn Speer, Joshua Chin, and Catherine Havasi. 2017. "ConceptNet 5.5: An Open Multilingual Graph of General Knowledge." In proceedings of AAAI 31.\n\n## Installation\n\n```bash\npip install conceptnet-rocks\n```\n\n## Usage\n\n### Install ArangoDB\n\nConceptNet Rocks uses [ArangoDB](https://www.arangodb.com/) for storage, managed by a companion Python [Graph Garden library](https://github.com/ldtoolkit/graph-garden/)  that is automatically installed with ConceptNet Rocks.\n\nGraph Garden can manage the ArangoDB installation for you. To download the latest version of ArangoDB from official website and install it to `~/.arangodb` folder, simply run:\n\n```bash\ngraph-garden arangodb install\n```\n\nFor more options execute:\n\n```bash\ngraph-garden arangodb install --help\n```\n\n### Load CSV dump into database\n\nThen you need to load the ConceptNet CSV dump into database. The dump can be downloaded from https://github.com/commonsense/conceptnet5/wiki/Downloads\n\nLet\'s assume you\'ve downloaded the dump to `~/conceptnet-data/assertions.csv`.\n\nTo load the dump, execute:\n```bash\nconceptnet-rocks-load ~/conceptnet-data/assertions.csv\n```\n\nThis command will create database in `~/.arangodb/data`. For more options execute:\n\n```bash\nconceptnet-rocks-load --help\n```\n\n### Run queries\n\nNow you can query ConceptNet. ConceptNet Rocks uses the same simple API as ConceptNet5 for querying:\n\n```python\nfrom conceptnet_rocks import AssertionFinder\n\naf = AssertionFinder()\nprint(af.lookup("/c/en/test"))\nprint(af.lookup("/r/Antonym"))\nprint(af.lookup("/s/process/wikiparsec/2"))\nprint(af.lookup("/d/wiktionary/en"))\nprint(af.lookup("/a/[/r/Antonym/,/c/ang/gecyndelic/a/,/c/ang/ungecynde/]"))\n```\n\nConceptNet Rocks uses the same JSON-LD format as the original ConceptNet5:\n```python\nfrom conceptnet_rocks import AssertionFinder\nfrom pprint import pprint\n\naf = AssertionFinder()\npprint(af.lookup("/c/en/blow_dryer"))\n# [\n# ...\n#  {\'@id\': \'/a/[/r/AtLocation/,/c/en/blow_dryer/,/c/en/beauty_salon/]\',\n#   \'@type\': \'Edge\',\n#   \'dataset\': \'/d/conceptnet/4/en\',\n#   \'end\': {\'@id\': \'/c/en/beauty_salon\',\n#           \'@type\': \'Node\',\n#           \'label\': \'a beauty salon\',\n#           \'language\': \'en\',\n#           \'term\': \'/c/en/beauty_salon\'},\n#   \'license\': \'cc:by/4.0\',\n#   \'rel\': {\'@id\': \'/r/AtLocation\', \'@type\': \'Relation\', \'label\': \'AtLocation\'},\n#   \'sources\': [{\'@id\': \'/and/[/s/activity/omcs/omcs1_possibly_free_text/,/s/contributor/omcs/bedume/]\',\n#                \'@type\': \'Source\',\n#                \'activity\': \'/s/activity/omcs/omcs1_possibly_free_text\',\n#                \'contributor\': \'/s/contributor/omcs/bedume\'}],\n#   \'start\': {\'@id\': \'/c/en/blow_dryer\',\n#             \'@type\': \'Node\',\n#             \'label\': \'a blow dryer\',\n#             \'language\': \'en\',\n#             \'term\': \'/c/en/blow_dryer\'},\n#   \'surfaceText\': \'You are likely to find [[a blow dryer]] in [[a beauty salon]]\',\n#   \'weight\': 1.0}\n# ...\n# ]\n```\n\n## FAQ\n\n### Why did you create yet another library if original ConceptNet5 exists?\n\n1. Performance. Our benchmark (https://github.com/ldtoolkit/conceptnet-benchmark) has shown that ConceptNet Rocks is\nalmost 5 times faster than ConceptNet5 for querying assertions by concepts.\n2. The original ConceptNet5 library requires PostgreSQL. PostgreSQL does not support the graph databases as a primary model, while ArangoDB is a multi-model database for graph.\n3. PostgreSQL generally requires either root permissions to install it using a package manager, or the compilation step. Not anyone have root permissions on their machine or have the compiler installed. ConceptNet Rocks library uses ArangoDB, which can be installed without root permissions using simple command.\n\n### Why is the library called ConceptNet Rocks?\n\n1. Under the hood ArangoDB uses key-value storage called RocksDB.\n2. Performance-wise, it does rock!\n',
    'author': 'Roman Inflianskas',
    'author_email': 'infroma@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ldtoolkit/conceptnet-rocks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

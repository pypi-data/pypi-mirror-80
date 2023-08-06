# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybeerxml']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pybeerxml',
    'version': '2.0.0',
    'description': 'A BeerXML implementation for Python',
    'long_description': '# pybeerxml\n\nA simple BeerXML parser for Python\n\n[![PyPi Version](https://img.shields.io/pypi/v/pybeerxml.svg?style=flat-square)](https://pypi.python.org/pypi?:action=display&name=pybeerxml)\n[![Build Status](https://img.shields.io/github/workflow/status/hotzenklotz/pybeerxml/Test%20and%20Lint/master)](https://github.com/hotzenklotz/pybeerxml/actions?query=branch%3Amaster+workflow%3A%22Test+and+Lint%22)\n[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\nParses all recipes within a BeerXML file and returns `Recipe` objects containing all ingredients,\nstyle information and metadata. OG, FG, ABV and IBU are calculated from the ingredient list. (your\nmilage may vary)\n\n## Installation\n\n```\npip install pybeerxml\n```\n\n## Usage\n\n```\nfrom pybeerxml import Parser\n\npath_to_beerxml_file = "/tmp/SimcoeIPA.beerxml"\n\nparser = Parser()\nrecipes = parser.parse(path_to_beerxml_file)\n\nfor recipe in recipes:\n\n    # some general recipe properties\n    print(recipe.name)\n    print(recipe.brewer)\n\n    # calculated properties\n    print(recipe.og)\n    print(recipe.fg)\n    print(recipe.ibu)\n    print(recipe.abv)\n\n    # iterate over the ingredients\n    for hop in recipe.hops:\n        print(hop.name)\n\n    for fermentable in recipe.fermentables:\n        print(fermentable.name)\n\n    for yeast in recipe.yeasts:\n        print(yeast.name)\n        \n    for misc in recipe.miscs:\n        print(misc.name)\n```\n\n## Testing\n\nUnit tests can be run with PyTest:\n\n```\npython -m pytest tests\n```\n\n## Contributing / Development\nCommunity contributions are welcome.\n\nDependency management is handled through [Poetry](https://python-poetry.org/):\n\n```\npip install poetry\n\npoetry install\n```\n\nMake sure to Test, Lint, Format, & Type-Check your code before sending a pull request:\n```\npython -m pytest tests\npython -m pylint pybeerxml\npython -m black pybeerxml\npython -m mypy pybeerxml\n```\n\n## License\n\nMIT\n',
    'author': 'Tom Herold',
    'author_email': 'heroldtom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hotzenklotz/picobrew-server',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdgen', 'mdgen.base']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=4.1.3,<5.0.0']

setup_kwargs = {
    'name': 'mdgen',
    'version': '0.1.2',
    'description': 'A library to generate random markdown text',
    'long_description': "# random-markdown-generator\n\nA library to generate random markdown text.\n\n## But why?\n\nI was making a blog web-app that lets its users write blog posts using markdown\nsyntax. I couldn't find any python package that does this easily. Using the\n[`faker`](https://github.com/joke2k/faker) library, I created this package to\nmake a highly configurable markdown post generator. Additionally, it also\nprovides an API for creating markdown files using python.\n\n## Getting Started\n\nThese instructions will get you a copy of the project up and running on your\nlocal machine for development and testing purposes.\n\n### Installing\n\nYou must have `python` and `pip` installed on your system, and in you `PATH`.\nAn activated virtual environment is also recommended.\n\nUsing `pip`:\n\n```bash\npip install mdgen\n```\n\nOr using poetry:\n\n```bash\npoetry add mdgen\n```\n\n## Sample usage\n\n```python\nfrom mdgen import MarkdownGenerator\n```\n\n## Running the tests\n\nThe project uses `pytest` to automate its test suite. To install all\ndependencies, ensure you have [`poetry`][1] installed on your system and then run:\n\n```bash\npoetry install\n```\n\nThis will install all dependencies for testing this project in a virtual\nenvironment. Then run all tests using:\n\n```bash\npoetry shell\npytest\n```\n\nTo see test coverage, run:\n\n```bash\npytest --cov --cov-report=html --cache-clear\n```\n\nThen open `htmlcov/index.html` in your browser to see the test coverage.\n\n### Coding style\n\nThis project follows the [Pep8](https://pep8.org/) specifications. The maximum\nline length has been increased to 90 characters. For the flake8 configuration\nused, see [tox.ini](tox.ini). The test suite automatically runs the linters by\ndefault, but you can run just the linting tests.\n\n```bash\nflake8\n```\n\n## Built With\n\n- [Poetry][1] - Dependency Management\n- [Mkdocs](https://www.mkdocs.org/) - Used to generate this project's\n  documentation.\n\n## Contributing\n\nPlease read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of\nconduct, and the process for submitting pull requests to us.\n\n## Versioning\n\nWe use [SemVer](http://semver.org/) for versioning.\n\n## Authors\n\n- [IgnisDa](https://github.com/IgnisDa/) (**Diptesh Choudhuri**) - _Initial\n  work_\n\nSee also the list of [contributors](contributors.md) who participated in this project. If you\nhave made any contribution to this project, please add it in\n[contributors.md](contributors.md)\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md)\nfile for details.\n\n## Acknowledgments\n\n- Hat tip to anyone whose code was used\n- Inspiration\n\n[1]: https://github.com/python-poetry/poetry\n",
    'author': 'IgnisDa',
    'author_email': 'ignisda2002@gmail.com',
    'maintainer': 'IgnisDa',
    'maintainer_email': 'ignisda2002@gmail.com',
    'url': 'https://github.com/IgnisDa/python-random-markdown-generator/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

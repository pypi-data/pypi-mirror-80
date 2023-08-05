# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polyanalyst6api']

package_data = \
{'': ['*']}

install_requires = \
['pytus>=0.2.1,<0.3.0', 'requests>=2.19,<3.0']

setup_kwargs = {
    'name': 'polyanalyst6api',
    'version': '0.16.0',
    'description': 'polyanalyst6api is a PolyAnalyst API client for Python.',
    'long_description': "# polyanalyst6api\n\n[![PyPI package](https://img.shields.io/pypi/v/polyanalyst6api.svg?)](https://pypi.org/project/polyanalyst6api)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/polyanalyst6api.svg?)](https://pypi.org/project/polyanalyst6api/)\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/Megaputer/polyanalyst6api-python/blob/master/LICENSE)\n\n`polyanalyst6api` is a Python library for interacting with PolyAnalyst APIs.\n\n## Installation\n\nPython 3.6+ is required. Install, upgrade and uninstall `polyanalyst6api-python` with these commands:\n\n```\n$ pip install polyanalyst6api\n$ pip install --upgrade polyanalyst6api\n$ pip uninstall polyanalyst6api\n```\n\n## Usage\n\nSee [API Reference](https://megaputer.github.io/polyanalyst6api-python/) for more detailed information.\n\n### Authentication\n\nImport client, initialize it and log in to PolyAnalyst's server:\n\n```python\nimport polyanalyst6api as polyanalyst\n\napi = polyanalyst.API(POLYANALIST_URL, USERNAME, PASSWORD)\napi.login()\n```\n\n`API` supports Context Manager protocol, so you could use it with `with` statement. In this case `API` will automatically log in with provided credentials.\n\n```python\nwith polyanalyst.API(POLYANALIST_URL, USERNAME, PASSWORD) as api:\n    pass\n```\n\n### Working with project\n\nSee [polyanalyst6api-python/examples](https://github.com/Megaputer/polyanalyst6api-python/tree/master/examples) for a more complex examples.\n\nAt first you need to connect to existing project:\n```python\nprj = api.project(PROJECT_UUID)\n```\n\nPrint node names within project:\n```python\nfor node_name in prj.get_nodes():\n    print(node_name)\n```\n\nInitiate node execution:\n```python\nprj.execute(NODE_NAME)\n```\n\nDisplay the preview of node results:\n```python\nresult = prj.preview(NODE_NAME)\nprint(result)\n```\n\nSave project:\n```python\nprj.save()\n```\n\n## PolyAnalyst API\nFull API specification is stored in the **PolyAnalyst User Manual** under the url below:\n\n```\n/polyanalyst/help/eng/24_Application_Programming_Interfaces/toc.html\n```\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details\n",
    'author': 'yatmanov',
    'author_email': 'yatmanov@megaputer.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Megaputer/polyanalyst6api-python/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

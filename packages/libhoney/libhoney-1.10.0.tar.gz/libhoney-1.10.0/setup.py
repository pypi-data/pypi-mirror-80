# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libhoney']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0', 'six>=1.15.0,<2.0.0', 'statsd>=3.3.0,<4.0.0']

extras_require = \
{':python_version >= "2.7" and python_version < "2.8"': ['futures>=3.3.0,<4.0.0',
                                                         'singledispatch>=3.4.0,<4.0.0',
                                                         'backports_abc>=0.5,<0.6']}

setup_kwargs = {
    'name': 'libhoney',
    'version': '1.10.0',
    'description': 'Python library for sending data to Honeycomb',
    'long_description': '# libhoney-py\n\n[![Build Status](https://circleci.com/gh/honeycombio/libhoney-py.svg?style=svg)](https://app.circleci.com/pipelines/github/honeycombio/libhoney-py)\n\nPython library for sending events to [Honeycomb](https://honeycomb.io), a service for debugging your software in production.\n\n- [Usage and Examples](https://docs.honeycomb.io/sdk/python/)\n- [API Reference](https://honeycombio.github.io/libhoney-py/)\n\nFor tracing support and automatic instrumentation of Django, Flask, AWS Lambda, and other frameworks, check out our [Beeline for Python](https://github.com/honeycombio/beeline-python).\n\n## Contributions\n\nFeatures, bug fixes and other changes to libhoney are gladly accepted. Please\nopen issues or a pull request with your change. Remember to add your name to the\nCONTRIBUTORS file!\n\nAll contributions will be released under the Apache License 2.0.\n\n## Releases\n\nYou may need to install the `bump2version` utility by running `pip install bump2version`.\n\nTo update the version number, do\n\n```\nbump2version [major|minor|patch|release|build]\n```\n\nIf you want to release the version publicly, you will need to manually create a tag `v<x.y.z>` and push it in order to\ncause CircleCI to automatically push builds to github releases and PyPI.\n',
    'author': 'Honeycomb.io',
    'author_email': 'feedback@honeycomb.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/honeycombio/libhoney-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)

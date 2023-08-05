# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virl2_client', 'virl2_client.models']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2,<3']

setup_kwargs = {
    'name': 'virl2-client',
    'version': '2.1.0rc1',
    'description': 'VIRL2 Client Library',
    'long_description': '# VIRL 2 Client Library\n\n## Introduction\n\nThis is the client library for the Cisco VIRL 2 Network Simulation Platform\n(`virl2_client`). It provides a Python package to programmatically create,\nedit, delete and control network simulations on a VIRL 2 controller.\n\nIt is a pure Python implementation that requires Python3. We\'ve tested and\nwritten the package with Python 3.6.8.\n\nThe **status** of this package can be considered **Beta**. We\'re not aware of\nany major issues at the time of release. However, since this is the first\nrelease of the package, bugs might exist. Both in the package as well as in\nthe API implementation on the controller.\n\n## Use Case Description\n\nThe client library provides a convenient interface to control the lifecycle of\na network simulation. This can be used for automation scripts directly in\nPython but also for third party integrations / plugins which need to integrate\nwith a simulated network. Examples already existing are an [Ansible\nplugin](https://github.com/CiscoDevNet/ansible-virl).\n\n## Installation\n\nThe package comes in form of a wheel that is downloadable from the VIRL 2\ncontroller. The package can be installed either from PyPi using\n\n    pip3 install virl2_client\n\nor, alternatively, the version that is bundled with the VIRL 2 controller can\nbe downloaded to the local filesystem and then directly installed via\n\n    pip3 install ./virl2_client-*.whl\n\nThe bundled version is available on the index site of the docs when viewed\ndirectly on the VIRL 2 controller.\n\nEnsure to replace use the correct file name, replacing the wildcard with the\nproper version/build information. For example\n\n    pip3 install virl2_client-2.0.0b10-py3-none-any.whl\n\nWe recommend the use of a virtual environment for installation.\n\n## Usage\n\nThe package itself is fairly well documented using docstrings. In addition, the\ndocumentation is available in HTML format on the controller itself, via the\n"Tools -> Client Library" menu.\n\n## Compatibility\n\nThis package and the used API is specific to VIRL 2. It is not\nbackwards compatible with VIRL 1.x and therefore can not be used with VIRL\n1.x. If you are looking for a convenient tool to interface with the VIRL 1 API\nthen the [VIRL Utils tool](https://github.com/CiscoDevNet/virlutils) is\nrecommended.\n\n## Known Issues\n\nThere are no known issues at this point. See the comment in the *Introduction*\nsection.\n\n## Getting Help\n\nIf you have questions, concerns, bug reports, etc., please create an issue\nagainst the [repository on\nGitHub](https://github.com/CiscoDevNet/virl2-client/)\n\n## Getting Involved\n\nWe welcome contributions. Whether you fixed a bug, added a new feature or\ncorrected a typo, all contributions are welcome. General instructions on how to\ncontribute can be found in the [CONTRIBUTING](CONTRIBUTING.md) file.\n\n## Licensing Info\n\nThis code is licensed under the Apache 2.0 License. See [LICENSE](LICENSE) for\ndetails.\n\n## References\n\nThis package is part of the VIRL 2 Network Simulation platform. For details, go\nto https://developer.cisco.com/modeling-labs. Additional documentation for the\nproduct is available at https://developer.cisco.com/docs/modeling-labs\n',
    'author': 'Simon Knight',
    'author_email': 'simknigh@cisco.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ciscodevnet/virl2-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5.0,<4.0.0',
}


setup(**setup_kwargs)

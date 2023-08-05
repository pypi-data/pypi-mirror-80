# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minisign', 'minisign.tests']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['minisign = minisign.__main__:run']}

setup_kwargs = {
    'name': 'minisign',
    'version': '0.1.0',
    'description': 'A dead simple tool to sign files and verify signatures',
    'long_description': "# Minisign Python\n\nThis is a pure Python implementation of [Frank Denis](https://twitter.com/jedisct1/)' [minisign](https://jedisct1.github.io/minisign/), following the [specifications](SPECS.md) copied from there.  \nCurrently following version *0.9*.\n\n**IMPORTANT NOTE**: this is currently under heavy development, and it hasn't undergone an external security assessment.\n\n## Goals\n\n* Compatible public interface: all commands and options must be 100% compatible and with same results.\n* Usage as CLI and as Python module.\n* Follow [semver](https://semver.org/).\n\n### Secondary goals\n\n* Small amount of dependencies (I would love to keep it just to cryptolibraries).\n* If possible, maintain current active Python versions (3.7+).\n\n## Milestones\n\n- [x] Define goals and license.\n- [x] Create initial project structure.\n   - [x] Code structure.\n   - [x] Contribution guidelines.\n   - [x] Pipeline.\n- [ ] Achieve basic functionality:\n   - [ ] Create key pair.\n   - [ ] Verify signature.\n   - [ ] Sign.\n- [ ] Ensure coverage 100%.\n- [ ] Make first release.\n- [ ] Add remaining options.\n\n## Requirements\n\n* Python 3.7+\n* PyNaCl 1.3+\n\n## License\n\n**Minisign Python** is made by [HacKan](https://hackan.net) under MPL v2.0. You are free to use, share, modify and share modifications under the terms of that [license](LICENSE).  Derived works may link back to the canonical repository: https://gitlab.com/hackancuba/minisign-py.  \n*Note that [minisign by Frank Denis](https://github.com/jedisct1/minisign/blob/master/LICENSE) is licensed under ISC*.\n\n    Copyright (C) 2020 HacKan (https://hackan.net)\n    This Source Code Form is subject to the terms of the Mozilla Public\n    License, v. 2.0. If a copy of the MPL was not distributed with this\n    file, You can obtain one at https://mozilla.org/MPL/2.0/.\n",
    'author': 'HacKan',
    'author_email': 'hackan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/hackancuba/minisign-py',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

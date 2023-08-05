# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['laika']

package_data = \
{'': ['*']}

install_requires = \
['dateparser>=0.7.0,<0.8.0', 'inquirer>=2.6,<3.0']

entry_points = \
{'console_scripts': ['laika = laika.cli:main',
                     'simple-git-deploy = laika.cli:main']}

setup_kwargs = {
    'name': 'laika-deploy',
    'version': '0.6',
    'description': 'A command-line utility for easy and reliable management of manual deployments from Git repositories',
    'long_description': '# Laika 🐶\n\n<a href="https://pypi.org/project/laika-deploy/" title="Available on PyPI">\n  <img src="https://img.shields.io/pypi/v/laika-deploy.svg?style=for-the-badge" alt="Latest PyPI version"></a>\n\nA command-line utility for easy and reliable management of manual deployments from Git repositories.\n\nEven manual deployments can be made reliable if some minimal automation is applied. This utility performs _atomic_ deployments from a Git repository, with an optional _build_ phase (e.g. installing dependencies). The previous deployment is not affected until the build completes successfully – no more inconsistency errors when you update your Git branch but your application is not yet fully updated – e.g. missing new dependencies from your package manager.\n\nEach deployment is built in a new directory made just for that deployment. Previous deployments are kept (and can be later purged), and the target is only updated when the build completes – that’s what we meant by _atomic_! If the build fails, the target will not be updated.\n\nThe meaning of _build_ is defined by the user; it can be any command runnable from a shell. Configuration is made in a simple `.ini` file.\n\n\n## Installation\n\nRequirements:\n\n* Python ≥ 3.6 (has been tested with 3.6 and 3.7)\n* Git ≥ 2.7 (depends on the `git worktree` feature)\n\nInstall via **pip**:\n\n```\n$ pip install laika-deploy\n```\n\nIf this fails and you have no idea what to do, you can try adding the `--user` option after `pip install`, though other options can be better in the long run – e.g. you can use [pipx][], or simply create a **virtualenv** for your installed scripts.\n\n\n## Usage\n\nAfter [installing this utility](#installation), you can run `laika --help` for basic usage instructions.\n\nThe easiest way is to run `laika deploy <git-branch-name>`. But before first usage you must create a `deploy.ini` file with at least the settings below (look further for an example):\n\n* `dirs.deploy`: directory where your application will be deployed. The current deployment will be available at `current` under this directory. This will be a symlink to the actual deployment directory.\n\n    So, for example, if you have a PHP application, you can point Nginx to the `/app/deployments/current` directory which will contain a working tree of your Git repository and will be updated whenever you deploy a new version, provided you add this to your `deploy.ini`:\n\n    ```ini\n    [dirs]\n    deploy = /app/deployments\n    ```\n\n    Each deployment will also live in this directory with a name containing the date/time of the deployment, the Git commit hash and the name of the branch/tag that was deployed.\n\n* `build.run`: which command to run in the _build_ phase. Typical usages are running your package manager, copying configuration files, compiling assets.\n\n    This is run as a shell command line – so you can chain commands as in `npm install && npm run build`.\n\nA complete configuration file would thus be:\n\n```ini\n[dirs]\ndeploy = /app/deployments\n\n[build]\nrun = npm install && npm run build\n```\n\n**It is assumed that the build will be run in the same host where the application is to be deployed.** Also, the user running this script must have **permission to write on the deployment directory**.\n\n\n### Purging old deployments\n\nYou can purge old deployments with `laika purge`. There are two ways to specify what exactly is to be removed:\n\n* `--keep-latest N`: keep only the latest _N_ deployments (other than the current one). With _N=0_, only the current deployment is kept, and with _N=1_ only one deployment other than the current is kept.\n* `--older-than DATETIME`: discard deployments with a timestamp strictly older than the given date/time. A wide range of both absolute and relative formats is accepted; see the [dateparser documentation](https://dateparser.readthedocs.io/en/latest/) for full information. Common cases may be written as `10d`, `1w` (10 days and 1 week, respectively).\n\n\n## Development setup\n\nIf you want to set this project up for development, see [CONTRIBUTING.md](./CONTRIBUTING.md).\n\n\n[pipx]: https://github.com/pipxproject/pipx/\n',
    'author': 'Eduardo Dobay',
    'author_email': 'edudobay@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/edudobay/laika',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)

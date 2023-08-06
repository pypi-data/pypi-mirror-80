# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argsearch']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.1,<2.0.0', 'tqdm>=4.49.0,<5.0.0']

entry_points = \
{'console_scripts': ['argsearch = argsearch:main']}

setup_kwargs = {
    'name': 'argsearch',
    'version': '0.2.1',
    'description': 'Run a command many times with different combinations of its inputs.',
    'long_description': '# argsearch\n`argsearch` is a simple and composable tool for running the same command many times with different combinations of arguments.\nIt aims to make random search and grid search easy for things like hyperparameter tuning and setting simulation parameters, while only requiring that your program accepts command line arguments in some form.\n\n## Example\n```\n$ argsearch grid 3 \'echo {a} {b}\' --a 0.0 1.5 --b X Y\n[\n{"args": {"a": "0.0", "b": "X"}, "command": "echo 0.0 X", "stdout": "0.0 X\\n", "stderr": "", "returncode": 0},\n{"args": {"a": "0.0", "b": "Y"}, "command": "echo 0.0 Y", "stdout": "0.0 Y\\n", "stderr": "", "returncode": 0},\n{"args": {"a": "0.75", "b": "X"}, "command": "echo 0.75 X", "stdout": "0.75 X\\n", "stderr": "", "returncode": 0},\n{"args": {"a": "0.75", "b": "Y"}, "command": "echo 0.75 Y", "stdout": "0.75 Y\\n", "stderr": "", "returncode": 0},\n{"args": {"a": "1.5", "b": "X"}, "command": "echo 1.5 X", "stdout": "1.5 X\\n", "stderr": "", "returncode": 0},\n{"args": {"a": "1.5", "b": "Y"}, "command": "echo 1.5 Y", "stdout": "1.5 Y\\n", "stderr": "", "returncode": 0}\n]\n```\n\n## Installation\n\n```\npip install argsearch\n```\n\n## Usage\n\n`argsearch` takes 3 kinds of arguments:\n - A **search strategy** (*random,* *grid,* or *repeat*) and its configuration:\n    - For *random*: **trials**, the number of random trials to run.\n    - For *grid*: **divisions**, the number of points to try in each numeric range.\n    - For *repeat*: **repeats**, the number of times to repeat the command.\n - A **command string** with **templates** designated by bracketed names (e.g. `\'python my_script.py --flag {value}\'`.\n -  A **range** for each template in the command string (e.g. `--value 1 100`).\n\nThen, `argsearch` runs the command string several times, each time replacing the templates with values from their associated ranges.\nNote that the *repeat* strategy does not admit templates or range arguments.\n\n### Search Strategies\n\nThree search strategies are currently implemented:\n - **Random search** samples uniformly randomly from specified ranges for a fixed number\n     of trials.\n - **Grid search** divides each numeric range into a fixed number of\n     evenly-spaced points and runs once for each possible combination of\n     inputs.\n - **Repeat** runs the same command a fixed number of times.\n\n### Ranges\nThree types of ranges are available:\n - **Floating-point ranges** are specified by a minimum and maximum floating-point value (e.g. `--value 0.0 1.0`).\n - **Integer ranges** are specified by a minimum and maximum integer (e.g. `--value 1 100`). Integer ranges are guaranteed to only yield integer values.\n - **Categorical ranges** are specified by a list of non-numeric categories, or more than two numbers (e.g. `--value A B C`, `--value 2 4 8 16`). Categorical ranges only draw values from the listed categories, and are not divided up during a grid search.\n\n### Output\n\nThe output is JSON, which can be wrangled with [jq](https://github.com/stedolan/jq) or other tools, or dumped to a file. The run is a list of mappings, one per command call, each of which has the following keys:\n - `args`: a mapping of argument names to values.\n - `command`: the command string with substitutions applied.\n - `stdout`: a string containing the command\'s stdout.\n - `stderr`: a string containing the command\'s stderr.\n - `returncode`: an integer return code for the command.\n',
    'author': 'Aidan Swope',
    'author_email': 'aidanswope@gmail.com',
    'maintainer': 'Aidan Swope',
    'maintainer_email': 'aidanswope@gmail.com',
    'url': 'https://github.com/maxwells-daemons/argsearch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

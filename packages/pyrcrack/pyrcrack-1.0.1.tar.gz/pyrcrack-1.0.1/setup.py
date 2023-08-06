# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrcrack']

package_data = \
{'': ['*']}

install_requires = \
['async-timeout>=3.0,<4.0',
 'docopt>=0.6.2,<0.7.0',
 'parse>=1.12,<2.0',
 'pytest-asyncio>=0.14.0,<0.15.0',
 'stringcase>=1.2,<2.0']

setup_kwargs = {
    'name': 'pyrcrack',
    'version': '1.0.1',
    'description': 'Pythonic aircrack-ng bindings',
    'long_description': 'pyrcrack\n--------\n\n**Python aircrack-ng bindings**\n\nPyrCrack is a Python API exposing a common aircrack-ng API. As AircrackNg will\nrun in background processes, and produce parseable output both in files and\nstdout, the most pythonical approach are context managers, cleaning up after \n\n.. image:: https://img.shields.io/pypi/l/pyrcrack\n.. image:: https://img.shields.io/librariesio/release/pypi/pyrcrack\n.. image:: https://img.shields.io/pypi/dm/pyrcrack\n.. image:: https://img.shields.io/pypi/pyversions/pyrcrack\n.. image:: https://img.shields.io/pypi/v/pyrcrack\n.. image:: https://codecov.io/gh/XayOn/pyrcrack/branch/develop/graph/badge.svg\n    :target: https://codecov.io/gh/XayOn/pyrcrack\n.. image:: https://github.com/XayOn/pyrcrack/workflows/CI%20commit/badge.svg\n    :target: https://github.com/XayOn/pyrcrack/actions\n\nInstallation\n------------\n\nThis library is available on `Pypi <https://pypi.org/project/pyrcrack/>`_, you can install it directly with pip::\n\n        pip install pycrack\n\nUsage\n-----\n\nThis library exports a basic aircrack-ng API aiming to keep always a small readable codebase.\n\nThis has led to a simple library that executes each of the aircrack-ng\'s suite commands\nand auto-detects its usage instructions. Based on that, it dinamically builds\nclasses inheriting that usage as docstring and a run() method that accepts\nkeyword parameters and arguments, and checks them BEFORE trying to run them.\n\nYou can find some example usages in examples/ directory::\n\n    async with pyrcrack.AircrackNg() as pcrack:\n        await pcrack.run(sys.argv[1])\n        # This also sets pcrack.proc as the running\n        # process, wich is a `Process` instance.\n\n        # get_result() is specific of AircrackNg class.\n        print(await pcrack.get_result())\n\n    # This will create temporary files needed, and\n    # cleanup process after if required.\n\nThere are some syntactic sugar methods, like "result_updater" on pyrcrack class.\n\nThe following example will automatically keep updating, for 10 seconds, a\nmeta["results"] property on pdump::\n\n    import pyrcrack\n    import sys\n    import asyncio\n    from async_timeout import timeout\n\n    async def test(max_timeout):\n        async with pyrcrack.AirodumpNg() as pdump:\n            with suppress(asyncio.TimeoutError):\n                async with timeout(max_timeout):\n                    await pdump.run(sys.argv[1])\n                    while True:\n                        await asyncio.sleep(1)\n                        print(pdump.meta)\n            return await pdump.proc.terminate()\n\n\n    asyncio.run(test(10))\n\nYou can also list all available airmon interfaces, like so::\n\n    async with pyrcrack.AirmonZc() as airmon:\n        print(await airmon.list_wifis())\n\nThis will return a nice dict with all information as is returned by airmon-zc\n',
    'author': 'David Francos',
    'author_email': 'opensource@davidfrancos.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

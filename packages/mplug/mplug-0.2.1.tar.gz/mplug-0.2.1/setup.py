# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mplug']

package_data = \
{'': ['*'], 'mplug': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['GitPython>=3.1.7,<4.0.0', 'requests>=2.24.0,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.7.0,<2.0.0']}

entry_points = \
{'console_scripts': ['mplug = mplug:run']}

setup_kwargs = {
    'name': 'mplug',
    'version': '0.2.1',
    'description': 'A plugin manager for mpv',
    'long_description': 'MPlug – a Plugin Manager for MPV\n================================\n\nA plugin manager for [mpv](https://mpv.io/) to easy install and uninstall mpv scripts and more.\n\nMotivation\n----------\nMpv is a great, free and open source video player. It has interfaces to extend\nit with different types of scripts and filters. There is a large number of\nawesome plugins: Watch [Youtube](https://youtube-dl.org/), [remove black bars](https://github.com/mpv-player/mpv/blob/master/TOOLS/lua/autocrop.lua), [improve the quality of Anime](https://github.com/bloc97/Anime4K),\n[remove noise from lecture recordings](https://github.com/werman/noise-suppression-for-voice), [skip adds](https://github.com/po5/mpv_sponsorblock)… The possibilities are endless.\n\nMPlug tries to make finding, installing and updating plugins as easy as possible.\n\nNote: The [underlying repository](https://github.com/Nudin/mpv-script-directory) of plugins is not (yet) complete, therefore not\nall plugins can be installed automatically so far. Please help [filling it](https://github.com/Nudin/mpv-script-directory/blob/master/HOWTO_ADD_INSTALL_INSTRUCTIONS.md).\n\nInstallation\n------------\nYou can install it via pip:\n```\n$ pip3 install mplug\n```\n\nAlternatively you can run it from the source:\n- Install dependencies: python3, [GitPython](https://pypi.org/project/GitPython/)\n- Clone this repository\n- Run with `run.py`\n\nUsage\n-----\n- You can find plugins in the WebUI of the [mpv script directory](https://nudin.github.io/mpv-script-directory/)\n- To install a plugin `mplug install plugin_name`\n- To update all plugins: `mplug upgrade`\n- To upgrade database: `mplug update`\n- To uninstall a plugin: `mplug uninstall plugin_id`\n- To disable a plugin without uninstalling it: `mplug disable plugin_id`\n- To search for a plugin `mplug search term`\n- To list all installed plugins `mplug list-installed`\n\nStatus & Todo\n-------------\n- [X] Populate mpv script directory, by scraping wiki\n- [X] First version of plugin manager\n- [X] Write a Webinterface to browse plugins\n- [ ] Add install instructions for **all** plugins to the [mpv script directory](https://github.com/Nudin/mpv-script-directory)\n- [ ] Write a TUI?\n- [ ] Write a GUI?\n',
    'author': 'Michael F. Schönitzer',
    'author_email': 'michael@schoenitzer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nudin/mplug',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['PyArr']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.21.0,<3.0.0']

setup_kwargs = {
    'name': 'pyarr',
    'version': '0.9.3',
    'description': 'A Sonarr and Radarr API Wrapper',
    'long_description': "# Sonarr and Radarr API Python Wrapper\n\nOriginal Sonarr wrapper from [SLiX69/Sonarr-API-Python-Wrapper](https://github.com/SLiX69/Sonarr-API-Python-Wrapper) which has been mostly re-written and Radarr added by myself.\n\nUnofficial Python Wrapper for the [Sonarr](https://github.com/Sonarr/Sonarr) and [Radarr](https://github.com/Radarr/Radarr) API.\n\nCurrently the package is under development, see the full [documentation](https://marksie1988.github.io/PyArr) for supported commands\n\n### Requirements\n\n- requests\n\n### Example Sonarr Usage:\n\n```\n# Import SonarrAPI Class\nfrom PyArr import SonarrAPI\n\n# Set Host URL and API-Key\nhost_url = 'http://your-domain.com'\n\n# You can find your API key in Settings > General.\napi_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'\n\n# Instantiate SonarrAPI Object\nsonarr = SonarrAPI(host_url, api_key)\n\n# Get and print TV Shows\nprint(sonarr.getSeries())\n```\n\n### Example Radarr Usage:\n\n```\n# Import RadarrAPI Class\nfrom PyArr import RadarrAPI\n\n# Set Host URL and API-Key\nhost_url = 'http://your-domain.com'\n\n# You can find your API key in Settings > General.\napi_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'\n\n# Instantiate RadarrAPI Object\nradarr = RadarrAPI(host_url, api_key)\n\n# Get and print TV Shows\nprint(radarr.getCalendar())\n```\n\n### Documentation\n\n- [PyArr Documentation](https://docs.totaldebug.uk/PyArr)\n- [Sonarr API Documentation](https://github.com/Sonarr/Sonarr/wiki/API)\n- [Radarr API Documentation](https://github.com/Radarr/Radarr/wiki/API)\n",
    'author': 'Steven Marks',
    'author_email': 'marksie1988@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/totaldebug/PyArr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

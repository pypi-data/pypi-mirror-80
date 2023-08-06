# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['web_youtube_dl', 'web_youtube_dl.app']

package_data = \
{'': ['*'],
 'web_youtube_dl': ['downloads/Si Veo a Tu Mamá - Bad Bunny ( Video Oficial '
                    ').mp3',
                    'downloads/Si Veo a Tu Mamá - Bad Bunny ( Video Oficial '
                    ').mp3',
                    "downloads/Vicente Fernández 'Ya me voy para siempre'.mp3",
                    "downloads/Vicente Fernández 'Ya me voy para siempre'.mp3"],
 'web_youtube_dl.app': ['static/*', 'templates/*']}

install_requires = \
['Werkzeug>=1.0.1,<2.0.0',
 'aiofiles>=0.5.0,<0.6.0',
 'cachetools>=4.1.1,<5.0.0',
 'fastapi>=0.61.0,<0.62.0',
 'janus>=0.5.0,<0.6.0',
 'jinja2>=2.11.2,<3.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'uvicorn>=0.11.8,<0.12.0',
 'youtube-dl>=2020.7.28,<2021.0.0']

entry_points = \
{'console_scripts': ['web-youtube-dl = web_youtube_dl.app.main:run_app',
                     'web-youtube-dl-cli = '
                     'web_youtube_dl.app.youtube_dl_helpers:cli_download']}

setup_kwargs = {
    'name': 'web-youtube-dl',
    'version': '0.1.0',
    'description': 'A web version of youtube-dl',
    'long_description': None,
    'author': 'Uriel Mandujano',
    'author_email': 'uriel.mandujano14@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

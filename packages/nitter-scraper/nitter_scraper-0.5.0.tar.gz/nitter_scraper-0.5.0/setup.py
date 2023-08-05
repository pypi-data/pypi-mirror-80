# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nitter_scraper']

package_data = \
{'': ['*'], 'nitter_scraper': ['templates/*']}

install_requires = \
['docker>=4.3.1,<5.0.0',
 'jinja2>=2.11.2,<3.0.0',
 'loguru>=0.5.1,<0.6.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.6.1,<2.0.0',
 'requests-html>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'nitter-scraper',
    'version': '0.5.0',
    'description': 'Scrape Twitter API without authentication using Nitter.',
    'long_description': '# Nitter Scraper\n\nNitter Scraper is for anyone who enjoys the [twitter-scraper](https://github.com/bisguzar/twitter-scraper/) library. Nitter Scraper leverages running a local docker container instance of [nitter](https://github.com/zedeus/nitter) to scrape a users tweets and profile information without the twitter api ratelimit. This api works similar to the [twitter-scraper](https://github.com/bisguzar/twitter-scraper/) project with a few differences.\n\n## Docker Engine\nFor the best experience use this library with [Docker Engine](https://docs.docker.com/engine/) properly installed. The NitterScraper manager will start, stop and remove a docker instance of [nitter](https://hub.docker.com/r/zedeus/nitter). If you can\'t run docker you can import the get_tweets and get_profile functions to scrape from [nitter.net](http://www.nitter.net).\n\n\n## Getting Started\n\n### Prereqs\n* Docker Engine\n* Python ^3.7\n\n### Install\n```shell\npip install nitter-scraper\n```\n\n#### How to Scrape a twitter users profile information.\n```python\nfrom pprint import pprint\n\nfrom nitter_scraper import NitterScraper\n\nwith NitterScraper(host="0.0.0.0", port=8008) as nitter:\n    profile = nitter.get_profile("dgnsrekt")\n    print("serialize to json\\n")\n    print(profile.json(indent=4))\n    print("serialize to a dictionary\\n")\n    pprint(profile.dict())\n\n```\n#### Output\n```python\n$ python3 examples/basic_usage.py\n2020-09-21 18:11:23.429 | INFO     | nitter_scraper.nitter:_get_client:31 - Docker connection successful.\n2020-09-21 18:11:25.102 | INFO     | nitter_scraper.nitter:start:135 - Running container infallible_noyce 91122c9b7b.\nserialize to json\n\n{\n    "username": "DGNSREKT",\n    "name": "DGNSREKT",\n    "profile_photo": "/pic/profile_images%2F1307990704384245760%2FSBVd3XT6.png",\n    "tweets_count": 2897,\n    "following_count": 904,\n    "followers_count": 117,\n    "likes_count": 4992,\n    "is_verified": false,\n    "banner_photo": "/pic/profile_banners%2F2474416796%2F1600684261%2F1500x500",\n    "biography": "BITCOIN IS DEAD AGAIN. :(",\n    "user_id": 2474416796,\n    "location": "Moon",\n    "website": "https://github.com/dgnsrekt"\n}\nserialize to a dictionary\n\n{\'banner_photo\': \'/pic/profile_banners%2F2474416796%2F1600684261%2F1500x500\',\n \'biography\': \'BITCOIN IS DEAD AGAIN. :(\',\n \'followers_count\': 117,\n \'following_count\': 904,\n \'is_verified\': False,\n \'likes_count\': 4992,\n \'location\': \'Moon\',\n \'name\': \'DGNSREKT\',\n \'profile_photo\': \'/pic/profile_images%2F1307990704384245760%2FSBVd3XT6.png\',\n \'tweets_count\': 2897,\n \'user_id\': 2474416796,\n \'username\': \'DGNSREKT\',\n \'website\': \'https://github.com/dgnsrekt\'}\n2020-09-21 18:11:25.905 | INFO     | nitter_scraper.nitter:stop:139 - Stopping container infallible_noyce 91122c9b7b.\n2020-09-21 18:11:31.284 | INFO     | nitter_scraper.nitter:stop:142 - Container infallible_noyce 91122c9b7b Destroyed.\n\n\n```\n#### Next step run the [examples](https://nitter-scraper.readthedocs.io/en/latest/examples/)\n\n## NitterScraper Limitation\n\n* About max 800 tweets per user.\n* Unable to scrape trends from nitter.\n* To scrape the user_id the user must have a banner photo. If the banner photo url isn\'t present\nthe user_id will be none.\n* The user_id cannot be scraped from the tweets.\n* birthday and is_private are not implemented in the profile.\n\n## Contact Information\nTelegram = Twitter = Tradingview = Discord = @dgnsrekt\n\nEmail = dgnsrekt@pm.me\n',
    'author': 'dgnsrekt',
    'author_email': 'dgnsrekt@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://nitter-scraper.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

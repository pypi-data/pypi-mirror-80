# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cloudflare_dyndns']
install_requires = \
['click>=7.0,<8.0', 'cloudflare>=2.3,<3.0', 'requests>=2.22,<3.0']

entry_points = \
{'console_scripts': ['cloudflare-dyndns = cloudflare_dyndns:main']}

setup_kwargs = {
    'name': 'cloudflare-dyndns',
    'version': '2.1',
    'description': 'CloudFlare Dynamic DNS client',
    'long_description': '# CloudFlare Dynamic DNS client\n\nThis is a simple Dynamic DNS script written in Python for updating CloudFlare DNS A records,  \nsimilar to the classic [ddclient perl script](https://sourceforge.net/p/ddclient/wiki/Home/).\n\n- You can run it as a cron job or a systemd timer.\n- It only updates the records if the IP address actually changed by storing a\n  cache of the current IP address.\n- It checks multiple IP services. If one of them doesn\'t respond, it skips it and check the next.\n- It has an easy to use command line interface.\n\n## Install\n\nIf you want to just use it, you can [download a standalone binary from the releases page.](https://github.com/kissgyorgy/cloudflare-dyndns/releases/)\n\nOr you can use [the Docker image](https://hub.docker.com/repository/docker/kissgyorgy/cloudflare-dyndns):\n\n```bash\n$ docker run --rm -it kissgyorgy/cloudflare-dyndns --help\n```\n\n## Development\n\nYou can install dependencies with poetry (preferable in a virtualenv).  \nAfter [installing poetry](https://poetry.eustace.io/docs/#installation), simply run:\n\n```bash\n$ poetry install\n```\n\n## Command line interface\n\n```bash\n$ cloudflare-dyndns --help\nUsage: cloudflare-dyndns [OPTIONS] [DOMAINS]\n\n  A simple command line script to update CloudFlare DNS A records with the\n  current IP address of the machine running the script.\n\n  For the main domain (the "@" record), simply put "example.com"\n  Subdomains can also be specified, eg. "*.example.com" or "sub.example.com"\n\nOptions:\n  --domains TEXT     The list of domains to update, separated by whitespace.\n                     It has to be ONE argument, so don\'t forget to quote! Can\n                     be set with the CLOUDFLARE_DOMAINS environment variable.\n\n  --email TEXT       CloudFlare account email. Can be set with\n                     CLOUDFLARE_EMAIL environment variable  [required]\n\n  --api-key TEXT     CloudFlare API key (You can find it at My Profile page).\n                     Can be set with CLOUDFLARE_API_KEY environment variable.\n                     [required]\n\n  --cache-file FILE  Cache file  [default: ~/.cache/cloudflare-dynds/ip.cache]\n  --force            Delete cache and update every domain\n  --debug            More verbose messages and Exception tracebacks\n  --help             Show this message and exit.\n```\n\n# Changelog\n\n**v2.0** breaks backward compatibility for a PyPI release.\n\nThe script you need to run is now called `cloudflare-dyndns` and the cache file\nalso changed. You can delete the old cache manually, or you can leave it, it\nwon\'t cause a problem.\n\nThe Docker file entry point is changed, so if you pull the new image, everything\nwill work as before.\n',
    'author': 'Kiss György',
    'author_email': 'kissgyorgy@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kissgyorgy/cloudflare-dyndns',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

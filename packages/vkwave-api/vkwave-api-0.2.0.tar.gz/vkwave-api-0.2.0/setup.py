# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vkwave_api']

package_data = \
{'': ['*']}

install_requires = \
['vkwave']

setup_kwargs = {
    'name': 'vkwave-api',
    'version': '0.2.0',
    'description': 'Accessing VK API for humans.',
    'long_description': '# VKWave-API\n\nAccessing VK API for humans.\n\n## Install\n\n```sh\npip install vkwave-api\n```\n\n## Example\n```python\nfrom vkwave_api import API, run\n\nasync def main():\n    api = API("MY TOKEN")\n    vk = api.get_api()\n    me = await vk.users.get()\n    print(me)\n\nrun(main())\n```\n',
    'author': 'prostomarkeloff',
    'author_email': '28061158+prostomarkeloff@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

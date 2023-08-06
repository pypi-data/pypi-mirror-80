# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rich_sparklines']

package_data = \
{'': ['*']}

install_requires = \
['rich>=7.1.0,<8.0.0', 'sparklines>=0.4.2,<0.5.0']

setup_kwargs = {
    'name': 'rich-sparklines',
    'version': '0.1.5',
    'description': 'Integrate rich and sparklines libraries',
    'long_description': 'Something like this:\n\n```python\nimport os\nimport random\nimport time\n\nfrom rich.console import Console\n\nfrom rich_sparklines import Graph\n\nconsole = Console()\n\n\ndef main():\n    graph = Graph("connections", lambda: random.randint(0, 20))\n    while True:\n        graph.update()\n\n        os.system("cls")\n\n        console.print(graph)\n\n        time.sleep(1)\n\n\nif __name__ == "__main__":\n    main()\n```\n\nwill produce something like this:\n\n![Example](./example.png)\n',
    'author': 'Elliana',
    'author_email': 'me@mause.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

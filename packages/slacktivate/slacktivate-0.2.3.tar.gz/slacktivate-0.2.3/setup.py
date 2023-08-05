# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['slacktivate',
 'slacktivate.helpers',
 'slacktivate.input',
 'slacktivate.macros',
 'slacktivate.slack']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.2.0,<8.0.0',
 'backoff>=1.10.0,<2.0.0',
 'cleo>=0.8.1,<0.9.0',
 'comma>=0.5.3,<0.6.0',
 'jinja2>=2.11.2,<3.0.0',
 'python-dotenv>=0.14.0,<0.15.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.24.0,<3.0.0',
 'slack-scim>=1.1.0,<2.0.0',
 'slackclient>=2.8.0,<3.0.0',
 'yaql>=1.1.3,<2.0.0']

setup_kwargs = {
    'name': 'slacktivate',
    'version': '0.2.3',
    'description': 'Slacktivate is a Python library and Command-Line Interface to assist in the provisioning of a Slack workspace.',
    'long_description': '# Slacktivate\n\nA tool to easily provision users automatically on Slack workspaces.',
    'author': 'Jérémie Lumbroso',
    'author_email': 'lumbroso@cs.princeton.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jlumbroso/slacktivate',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['remarshal']
install_requires = \
['PyYAML>=5.3,<6.0',
 'cbor2>=5.1,<6.0',
 'python-dateutil>=2.8,<3.0',
 'tomlkit>=0.7,<0.8',
 'u-msgpack-python>=2.6,<3.0']

entry_points = \
{'console_scripts': ['cbor2cbor = remarshal:main',
                     'cbor2json = remarshal:main',
                     'cbor2msgpack = remarshal:main',
                     'cbor2toml = remarshal:main',
                     'cbor2yaml = remarshal:main',
                     'json2cbor = remarshal:main',
                     'json2json = remarshal:main',
                     'json2msgpack = remarshal:main',
                     'json2toml = remarshal:main',
                     'json2yaml = remarshal:main',
                     'msgpack2cbor = remarshal:main',
                     'msgpack2json = remarshal:main',
                     'msgpack2msgpack = remarshal:main',
                     'msgpack2toml = remarshal:main',
                     'msgpack2yaml = remarshal:main',
                     'remarshal = remarshal:main',
                     'toml2cbor = remarshal:main',
                     'toml2json = remarshal:main',
                     'toml2msgpack = remarshal:main',
                     'toml2toml = remarshal:main',
                     'toml2yaml = remarshal:main',
                     'yaml2cbor = remarshal:main',
                     'yaml2json = remarshal:main',
                     'yaml2msgpack = remarshal:main',
                     'yaml2toml = remarshal:main',
                     'yaml2yaml = remarshal:main']}

setup_kwargs = {
    'name': 'remarshal',
    'version': '0.14.0',
    'description': 'Convert between CBOR, JSON, MessagePack, TOML, and YAML',
    'long_description': None,
    'author': 'D. Bohdan',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

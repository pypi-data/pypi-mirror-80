# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snecs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'snecs',
    'version': '1.2.2',
    'description': 'A straightforward, nimble ECS for Python',
    'long_description': '.. image:: https://raw.githubusercontent.com/slavfox/snecs/master/docs/_static/snecs_logo.png\n   :align: center\n   :alt: snecs\n\n=====\nsnecs\n=====\n\nA straightforward, nimble ECS for Python.\n\n.. teaser-start\n\n|PyPI badge| |PyVersion badge| |PyImplementation badge| |Mypy badge| |License badge|\n\n``snecs`` is a pure Python 3.6+, dependency-free\n`ECS <https://snecs.slavfox.space/ecs/>`__ library,\nheavily inspired by Rust’s\n`Legion <https://github.com/TomGillen/legion>`__, and aiming to be as\nfast and easy-to-use as possible.\n\n.. |PyPI badge| image:: https://img.shields.io/pypi/v/snecs\n   :alt: PyPI\n   :target: https://pypi.org/project/snecs/\n\n.. |PyVersion badge| image:: https://img.shields.io/pypi/pyversions/snecs\n   :alt: PyPI - Python Version\n\n.. |PyImplementation badge| image:: https://img.shields.io/pypi/implementation/snecs\n   :alt: PyPI - Implementation\n\n.. |Mypy badge| image:: https://img.shields.io/badge/mypy-typed-informational\n   :alt: Mypy: checked\n   :target: http://mypy-lang.org/\n\n.. |License badge| image:: https://img.shields.io/github/license/slavfox/snecs\n   :alt: GitHub\n   :target: https://github.com/slavfox/snecs/blob/master/LICENSE\n\n.. teaser-end\n\nScroll down to learn more, or `check out the documentation!\n<https://snecs.slavfox.space>`_\n\nOverview\n========\n\n``snecs`` is an\n`ECS <https://en.wikipedia.org/wiki/Entity_component_system>`__ library,\nwritten from the ground up to be:\n\nStraightforward!\n----------------\n\nThe ``snecs`` API is designed to be both easy-to-use, and encourage cleanly\nstructured code. It follows a simple principle - functions do things,\nclasses represent things - in an attempt to reduce the incidence of\nantipatterns like\n`ClassesAsNamespaces <https://www.youtube.com/watch?v=o9pEzgHorH0>`__.\n\nNimble!\n-------\n\n``snecs`` is written with a benchmark-driven approach. Every statement in\nthe hot path is benchmarked against alternative ways to express the same\nbehavior, to let your code run as fast as you need it to.\n\nOne of the design goals is outrunning\n`esper <https://github.com/benmoran56/esper>`__, and eventually I’ll\nhave a benchmark suite to post here.\n\nDependency-free!\n----------------\n\n``snecs`` has `no dependencies\nwhatsoever <https://github.com/slavfox/snecs/blob/master/pyproject.toml>`__,\nother than Python 3.6 or higher; you won’t need to worry about\ndeprecation warnings from dependencies, or having to install systemwide\nlibraries for dependencies to work - because there are none! Installing\nsnecs is as simple as running:\n\n.. code:: console\n\n   $ pip install snecs\n\nPure Python!\n------------\n\n``snecs`` is written entirely in Python. It does not use any modules written\nin C or any other language, which means that you don’t have to worry\nabout needing a C compiler if there are no wheels for your platform and\ndistribution, and that it **works perfectly under PyPy**, and gets the\nfull benefit of its JIT compiler and optimizations.\n\nFully typed!\n------------\n\n``snecs`` is checked against a `very aggressive mypy\nconfiguration <https://github.com/slavfox/snecs/blob/master/mypy.ini>`__\nto catch bugs and let you fully enjoy the library even when writing\ntype-annotated code. You won’t have to ``# type: ignore`` any use of\nsnecs.\n\nLovingly-commented!\n-------------------\n\nOver a third of the non-blank lines in the ``snecs/`` directory are\ncomments. If you ever need to dive into the code to see how ``snecs`` works\nunder the hood, they will guide you through the source and explain every\nworkaround, optimization, and obscure trick you might find non-obvious.\n\nLicense\n=======\n\n``snecs`` is made available under the terms of the Mozilla Public License\nVersion 2.0, the full text of which is available\n`here <https://www.mozilla.org/en-US/MPL/2.0/>`__, and included in\n`LICENSE <https://github.com/slavfox/snecs/blob/master/LICENSE>`__. If\nyou have questions about the license, check Mozilla’s `MPL\nFAQ <https://www.mozilla.org/en-US/MPL/2.0/FAQ/>`__.\n',
    'author': 'Slavfox',
    'author_email': 'slavfoxman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/slavfox/snecs',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

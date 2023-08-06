# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['duckdb_engine', 'duckdb_engine.tests']

package_data = \
{'': ['*']}

install_requires = \
['duckdb>=0.2.1,<0.3.0', 'sqlalchemy>=1.3.19,<2.0.0']

entry_points = \
{'sqlalchemy.dialects': ['duckdb = duckdb_engine']}

setup_kwargs = {
    'name': 'duckdb-engine',
    'version': '0.1.0',
    'description': '',
    'long_description': '# duckdb_engine\n\nVery very very basic sqlalchemy driver for duckdb\n\nOnce you install this package, you should be able to just use it, as sqlalchemy does a python path search\n\n```python\nfrom sqlalchemy import Column, Integer, Sequence, String, create_engine\nfrom sqlalchemy.ext.declarative import declarative_base\nfrom sqlalchemy.orm.session import Session\n\nBase = declarative_base()\n\n\nclass FakeModel(Base):  # type: ignore\n    __tablename__ = "fake"\n\n    id = Column(Integer, Sequence("fakemodel_id_sequence"), primary_key=True)\n    name = Column(String)\n\n\neng = create_engine("duckdb:///:memory:")\nBase.metadata.create_all(eng)\nsession = Session(bind=eng)\n\nsession.add(FakeModel(name="Frank"))\nsession.commit()\n\nfrank = session.query(FakeModel).one()\n\nassert frank.name == "Frank"\n```\n',
    'author': 'Elliana',
    'author_email': 'me@mause.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

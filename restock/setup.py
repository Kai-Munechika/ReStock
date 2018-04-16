from setuptools import setup

setup(
    name='restock',
    author="Kai Munechika, Helen Zhang",
    packages=['restock',
              'restock.controller',
              'restock.model',
              'restock.util',
              'restock.web',
              'restock.db'],
    include_package_data=True,
    install_requires=['flask',
                      'requests',
                      'pymongo',
                      'queuelib'],
)

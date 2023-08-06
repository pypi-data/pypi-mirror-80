import os
import re
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_version():
    res = read(os.path.join('psk-escpos', '__init__.py'))
    return re.search("__version__ = '([0-9.]*)'", res).group(1)


setup(
    name='psk-escpos',
    version=get_version(),
    author='Camilo Sarmiento',
    author_email='camilosarmiento777@gmail.com',
    url="https://bitbucket.org/developer_presik/psk-escpos/src/master/",
    description="Python Library for pos printer",
    download_url="https://bitbucket.org/developer_presik/psk-escpos/src/master/",
    keywords=['presik', 'psk', 'escpos', 'printer'],
    packages=find_packages(),
    package_data={
        'psk-escpos': {
            'capabilities-data': (['data/*.yml', 'data/profile/*.yml', 'scripts/*.py']),
            'src': (['escpos/*.py', 'escpos/*.json']),
            },
    },
    test_suite='psk-escpos.tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Printing',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='LGPL',
    use_2to3=True)

from distutils.core import setup
import glob
from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'readme.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nwscapparser3',
    version='3.0.5',
    # 3.0.5 - added CAPEntry.dict() so that items can be easily json-ized

    description='NWS CAP Parser for Python3',
    long_description=long_description,
    author='Grant Miller. Based on the work of Robert Morris (robert@emthree.com)',
    author_email='grant@grant-miller.com',
    url='https://github.com/GrantGMiller/NWS-CAP-parser',
    packages=['nwscapparser3'],
    license="PSF",
    keywords="python3 cap common alert protocol grant miller robert morris xml",
    install_requires=['requests', 'lxml'],
    data_files=[
        ('', glob.glob('*.xml')),
        ('', ['demo.py', 'readme.rst', 'LICENSE'])]
)

# to push to PyPI

# python -m setup.py sdist bdist_wheel
# twine upload dist/*

from setuptools import setup
from sblpy import __version__

try:
    with open("./README.md") as rfile:
        long = rfile.read()
except:
    long = ""

setup(
    name='SBLPy',
    version=__version__,
    packages=['sblpy'],
    url='https://github.com/EEKIM10/sblpy',
    license='MIT',
    author='EEKIM10',
    author_email='eek@clicksminuteper.net',
    description='SBLP\'s HTTP system, wrapped into python',
    long_description=long,
    long_description_content_type='text/markdown',
)

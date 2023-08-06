# vim: expandtab tabstop=4 shiftwidth=4

from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name='minnow',
    version='2020.272.0',
    author='Bill Allen',
    author_email='photo.allen@gmail.com',
    description='Utilities for the Minnow file processing framework.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='minnow file processing properties'.split(),
    url='https://github.com/gershwinlabs/minnow-python',
    packages=['minnow'],
    install_requires=['setuptools'],
    python_requires='>=3.5, <4',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License'
    ]
)

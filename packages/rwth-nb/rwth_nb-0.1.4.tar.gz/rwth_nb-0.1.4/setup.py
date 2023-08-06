#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def get_version():
    """
    Read git tag and version given by environment variable and convert it to a version number.
    The build will only be processed if you are standing at a clean tag, as this will result in 
    a clean versioning scheme.
    :return:
    """
    import subprocess

    try:
        git_describe = subprocess.check_output(["git", "describe", "--tags"])
        git_describe = git_describe.decode("utf-8").strip()

        f = open('version.txt','w')
        f.write(git_describe)
        f.close()
        # and do it one more for packaging if possible
        # f = open('src/rwth-nb/version.txt','w')
        # f.write(git_describe)
        # f.close()
    except:
        f = open('version.txt','r')
        git_describe = f.readline()
        f.close()

    version = git_describe
    split_describe = git_describe.split('-')
    if (len(split_describe) > 1):
        raise Exception("I do not want to build this package since you did not tag your current state of work.")

    return version


setup(name='rwth_nb',
      # Versions should comply with PEP440.  For a discussion on single-sourcing
      # the version across setup.py and the project code, see
      # https://packaging.python.org/en/latest/single_source_version.html
      version=get_version(),
      description='RWTH Python Library for Jupyter Notebooks',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://git.rwth-aachen.de/jupyter/rwth-nb',
      author='Christian Rohlfing, Lars Thieling, Christoph Weyer, Jens Schneider, Steffen Vogel',
      author_email='rohlfing@ient.rwth-aachen.de',
      license='MIT',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      install_requires=[], # todo
      zip_safe=False)

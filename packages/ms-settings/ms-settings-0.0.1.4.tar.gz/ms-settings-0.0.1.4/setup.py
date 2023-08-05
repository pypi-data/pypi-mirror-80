import os

from setuptools import setup

from ms_settings import __version__


def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()


def git_version():
    """
    Fetch version from git information
    """
    return '.'.join([str(u) for u in __version__])


setup(name="ms-settings",
      version=git_version(),
      description="A simple setting tool for project",
      long_description=read_file('README.md'),
      long_description_content_type='text/markdown',
      url='http://gitlab.com/liang.guisheng/py_settings',
      author='Liang Guisheng',
      author_email='theol.liang@gmail.com',
      license='MIT',
      classifiers=[
          'Programming Language :: Python :: 3',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
      ],
      keywords='python settings configuration',
      packages=["ms_settings"],
      extras_require={'dev': read_file('requirements-dev.txt').strip().split('\n')[1:]})

"""Install Natural Questions."""
from setuptools import find_packages
from setuptools import setup

setup(
    name='natural-questions',
    version='1.0.6',
    description='Natural Questions',
    author='Google Inc.',
    author_email='no-reply@google.com',
    url='https://github.com/google-research-datasets/natural-questions',
    license='Apache 2.0',
    packages=find_packages(),
    install_requires=['absl-py', 'jinja2', 'tornado'],
)

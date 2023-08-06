from setuptools import setup
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as f:
    readme = f.read()

setup(
    name='pybicpl',
    version='0.1-1',
    py_modules=['pybicpl'],
    url='https://github.com/FNNDSC/pybicpl',
    license='MIT',
    author='Jennings Zhang',
    author_email='Jennings.Zhang@childrens.harvard.edu',
    description='Python interface for basic MNI .obj file format. '
                'Supports read, write, and calculations on a vertex neighbor graph.',
    install_requires=['numpy~=1.19.0'],
    python_requires='>=3.6',
)

from setuptools import setup, find_packages
from os import path
from io import open


# Reading the README.md file and adding to package
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


# Package setup definition
setup(
    author_email='bryan.cruz@mandic.net.br',
    author='Bryan Cruz',
    description='The multi cloud security group analyzer',
    entry_points={
        'console_scripts': [
            'panoptesctl = mandic_panoptes.panoptesctl:main',
        ],
    },
    install_requires=[
        'boto3==1.9.28',
        'click==7.0',
        'colorama==0.4.0',
        'PyYAML==3.13',
        'Jinja2==2.10',
    ],
    keywords='panoptes aws security analysis cloud devops',
    license='LICENSE',
    long_description_content_type='text/markdown',
    long_description=long_description,
    name='mandic_panoptes',
    packages=find_packages(),
    python_requires='>=3.6',
    url='https://gitlab.com/rivendel-cmp/panoptes',
    version='0.6.0',
)

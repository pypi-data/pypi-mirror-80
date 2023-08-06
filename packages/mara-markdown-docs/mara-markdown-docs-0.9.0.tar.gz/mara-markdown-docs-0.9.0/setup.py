from setuptools import setup, find_packages
import re


def get_long_description():
    with open('README.md') as f:
        return re.sub('!\[(.*?)\]\(docs/(.*?)\)',
                      r'![\1](https://github.com/jankatins/mara-markdown-docs/raw/master/docs/\2)', f.read())


setup(
    name='mara-markdown-docs',
    version='0.9.0',

    description='Display markdown documentation in mara UI',

    long_description=get_long_description(),
    long_description_content_type='text/markdown',

    url='https://github.com/jankatins/mara-markdown-docs',

    install_requires=[
        'mara-app>=2.2.0',
    ],
    tests_require=['pytest'],

    python_requires='>=3.7',

    packages=find_packages(),

    author='Mara contributors',
    license='MIT',

    entry_points={},
)

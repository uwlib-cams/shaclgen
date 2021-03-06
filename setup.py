# -*- coding: utf-8 -*-
#%%
from setuptools import setup


with open('README.rst') as readme:
    l_description = readme.read()
with open('requirements.txt') as reqs:
    requirements = reqs.read()

setup(
    name = 'shaclgen',
    version = '0.2.5.2',
    packages = ['shaclgen'],
    package_data = {'shaclgen': ['prefixes/*.json']},
    description='Shacl graph generator',
    long_description=l_description,
    author='Alexis Keely',
    url='https://github.com/uwlib-cams/shaclgen',
    author_email='alexiskeelie@gmail.com',
    install_requires=requirements,
    keywords=['Linked Data', 'Semantic Web', 'Python',
              'SHACL', 'Shapes', 'Schema', 'Validate'],
    license='MIT',
    classifiers=[
                'Development Status :: 4 - Beta',
                'Programming Language :: Python :: 3',

    ],
    entry_points = {
        'console_scripts': [
            'shaclgen = shaclgen.__main__:main'
        ]
    })

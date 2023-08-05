#!/usr/bin/env python
# coding=utf-8
# 
# to build:
#   python setup.py sdist bdist_wheel
# 

from setuptools import setup, find_packages

setup(
    name='co_excitation_gas_modeling',
    version='0.0.1',
    description=(
        'A Python Package for Galaxy Cold Molecular Gas Density Esimtation from CO Excitation.'
    ),
    keywords="co excitation galaxy molecular gas density temperature",
    long_description=open('README.rst').read(),
    author='DLIU',
    author_email='dzliu@mpia.de',
    maintainer='DLIU',
    maintainer_email='dzliu@mpia.de',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://sites.google.com/view/co-excitation-gas-modeling',
    project_urls={
        #"Bug Tracker": "https://bugs.example.com/HelloWorld/",
        "Documentation": "https://sites.google.com/view/co-excitation-gas-modeling",
        #"Source Code": "https://code.example.com/HelloWorld/",
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Astronomy',
    ],
    install_requires=[
        'numpy',
        'astropy',
        'matplotlib',
        'funcsigs; python_version<"3.0"',
    ], 
    include_package_data=True,
    #package_data={
    #    'project': ['default_data.json', 'other_datas/default/*.json']
    #},
    #data_files=
)


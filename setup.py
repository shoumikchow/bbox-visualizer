#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = []

setup_requirements = []

test_requirements = []

setup(
    author="Shoumik Sharar Chowdhury",
    author_email='shoumikchow@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Different ways of visualizing objects given bounding box data",
    install_requires=requirements,
    license="MIT license",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='bbox_visualizer',
    name='bbox_visualizer',
    packages=find_packages(include=['bbox_visualizer', 'bbox_visualizer.*']),
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    url='https://github.com/shoumikchow/bbox-visualizer',
    version='0.1.0',
    zip_safe=False,
)

from __future__ import annotations

import typing

from setuptools import setup, find_packages


package_name = 'best_testrail_client'


def get_version() -> typing.Optional[str]:
    with open('best_testrail_client/__init__.py', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('__version__'):
            return line.split('=')[-1].strip().strip("'")


def get_long_description() -> str:
    with open('README.md', encoding='utf8') as f:
        return f.read()


setup(
    name=package_name,
    description='TestRail client implementing all API v2.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords='testrail test report',
    version=get_version(),
    author='Valery Pavlov',
    author_email='lerikpav@gmail.com',
    install_requires=[
        'setuptools',
        'requests>=2.22.0',
        'typing_extensions>=3.7.2',
    ],
    url='https://github.com/best-doctor/best_testrail_client',
    license='MIT',
    py_modules=[package_name],
    zip_safe=False,
)

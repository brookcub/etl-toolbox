import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

import etl_toolbox

with open("README.rst", "r") as r:
    long_description = r.read()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ["--doctest-modules",
                          "--cov=etl_toolbox",
                          "--doctest-glob=*.rst",
                          "--ignore=docs/conf.py"]
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name='etl-toolbox',
    version=etl_toolbox.__version__,
    author='Brooklyn Rose Ludlow',
    description='Useful ETL functions for Python',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://etl-toolbox.readthedocs.io',
    project_urls={
        "Source Code": "https://github.com/brookcub/etl-toolbox",
        "Bug Reports": "https://github.com/brookcub/etl-toolbox/issues",
        "Documentation": "https://etl-toolbox.readthedocs.io",
    },
    keywords='etl pandas data cleaning',
    license='Apache-2.0',
    packages=['etl_toolbox'],
    install_requires=['numpy>=1.18.0',
                      'pandas>=0.25.0'
                      ],
    python_requires='>=3.5',
    tests_require=['pytest',
                   'coverage',
                   'pytest-cov'
                   ],
    cmdclass={'test': PyTest},
    platforms='any',
    test_suite='etl_toolbox.test.test_etl_toolbox',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
    extras_require={
        'testing': ['pytest'],
    }
)

import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

import etl_toolbox

with open("README.rst", "r") as r:
    long_description = r.read()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ["--doctest-modules", "--cov=."]
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
    url='https://github.com/brookcub/etl-toolbox',
    keywords='etl pandas data cleaning',
    license='Apache Software License',
    packages=['etl_toolbox'],
    install_requires=['numpy>=1.18.0',
                      'pandas>=1.0.0'
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
        'Programming Language :: Python :: 3',
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

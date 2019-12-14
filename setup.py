import sys
from setuptools import setup

if sys.version_info < (3, 7):
    raise Exception("Please use Python 3.7 or higher to install")

setup(
    name='open_weather_api',
    version='1.0.0',
    url='https://github.com/cdgriffith/open_weather_api',
    author='Chris Griffith',
    tests_require=["pytest", "coverage >= 3.6", "pytest-cov"],
    install_requires=['python-box', 'reusables', 'requests', 'appdirs'],
    author_email='chris@cdgriffith.com',
    description='Open Weather API',
    packages=['open_weather_api', 'test'],
    py_modules=['open_weather_cli'],
    include_package_data=True,
    platforms='any',
    setup_requires=['pytest-runner'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    extras_require={
        'testing': ["pytest", "coverage >= 3.6", "pytest-cov"],
    },
    entry_points={
        'console_scripts': ['forecast=open_weather_cli:main'],
    }
)

from setuptools import  setup, find_packages

setup(
    name    = 'pypi-sample',

    version = '0.1',

    description = 'for sample about doople pypi project',

    author = 'doople',

    author_email = 'log@doople.net',

    url = 'https://github.com/log-kim/test-pypi.git',

    download_url = '',

    install_requires = [],

    package = find_packages(exclude=[]),

    keywords = ['pypi deploy'],

    python_requires = '>=3',

    package_data = {},

    zip_safe = False,

    classifiers = [
        'Programming Language :: Python :: 3.7'
    ]
)
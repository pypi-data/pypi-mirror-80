from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name = 'puid',
    version = '0.0.1',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    url = 'https://github.com/edsu/puid',
    py_modules = ['puid',],
    description = 'Lookup a PRONOM Unique Identifier for a file.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = ['opf-fido'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)

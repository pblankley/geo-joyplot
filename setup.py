from distutils.core import setup

setup(
    name='geo_joyplot',
    version='0.1.0',
    author='Paul Blankley',
    author_email='pablankley@gmail.com',
    packages=['geo_joyplot'],
    description='Library for mapping lat long square to joyplot',
    long_description=open('README.md').read(),
    install_requires=[
        "pandas >= 0.22.0",
        "numpy >= 1.13.3",
        "joypy >= 0.1.9",
        "matplotlib >= 2.1.2",
    ],
)

from setuptools import setup

long_description = open('README.md').read()

setup(
    name='pyversasense',
    version='0.0.1',
    description='Versasense API consumer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/flamm3blemuff1n/pyversasense',
    author='Steven Impens',
    author_email='s.impens.dev@gmail.com',
    license='Apache License 2.0',
    packages=['pyversasense'],
    zip_safe=True,
    install_requires=['aiohttp>=3.5.4'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License"
    ],
)
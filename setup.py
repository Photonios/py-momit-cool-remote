import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(
    name='py-momit-cool-remote',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Library for remotely interfacing with the Momit Cool air conditioning controller.',
    long_description=README,
    url='https://github.com/Photonios/py-momit-cool-remote',
    author='Swen Kooij',
    author_email='swenkooij@gmail.com',
    keywords=['momit', 'cool', 'remote', 'control'],
    entry_points={
        'console_scripts': [
            'momit-cool=cli:main'
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)

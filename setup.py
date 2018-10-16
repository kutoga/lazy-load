import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="lazy_load",
    version="0.8.2",
    url="https://github.com/kutoga/lazy-load",
    license='MIT',

    author="Benjamin Bruno Meier",
    author_email="benjamin.meier70@gmail.com",

    description="ℒazy-ℒoad - A minimalistic interface that allows the lazy evaluation " +\
                "of expressions. Additional functions and wrappers allow it to easily " +\
                "use the lazy evaluation for functions and classes.",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests',)),

    install_requires=['lazy-object-proxy>=1.3.1'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)


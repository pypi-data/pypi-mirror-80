from setuptools import setup
import pypandoc

with open('./README.md', encoding='utf-8') as f:
    long_description = f.read()

# rst_description = pypandoc.convert_text(long_description, 'rst', format='markdown_github')

setup(
    name = "sout",
    version = '1.0.3',
    description = 'This package provides a simple output of python objects.',
    author = 'bib_inf',
    author_email = 'contact.bibinf@gmail.com',
    url = 'https://github.co.jp/',
    packages = ["sout"],
    install_requires = ["relpath"],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license="CC0 v1.0",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    ]
)

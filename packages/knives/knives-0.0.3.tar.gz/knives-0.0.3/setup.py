import setuptools
from knives import __version__ as knives_version

with open('Readme.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='knives',
    version=knives_version,
    author='owtotwo',
    author_email='owtotwo@163.com',
    description='A commonly used python tools library for myself',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/owtotwo/knives',
    py_modules=['knives'],
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: Microsoft :: Windows :: Windows 10',
    ],
    python_requires='>=3.7',
)

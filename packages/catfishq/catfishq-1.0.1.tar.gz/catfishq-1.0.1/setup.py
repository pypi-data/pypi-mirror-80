"""
CatfishQ

"""
import os
from setuptools import setup

__version__ = '1.0.1'

setup(
    name='catfishq',
    version=__version__,
    author='philres',
    description='Cat FASTQ files',
    zip_safe=False,
    install_requires=[
        'pysam'
    ],
    packages=[
        'catfishq'
    ],
    entry_points={
        "console_scripts": [
            'catfishq = catfishq.cat_fastq:main',
        ]
    },
)

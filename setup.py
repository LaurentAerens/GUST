
from setuptools import setup, find_packages

setup(
    name="gust",
    version="0.1.0",
    packages=find_packages(where="source"),
    package_dir={"": "source"},
    install_requires=[],
    entry_points={
        'console_scripts': [
            'gust=source.main:main',
        ],
    },
    author="Laurent Aerens",
    description="Genetic Universal Stockfish Trainer",
    license="GNU General Public License v3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
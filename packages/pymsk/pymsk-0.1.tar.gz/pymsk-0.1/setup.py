import setuptools
from pathlib import Path

setuptools.setup(
    # package info
    name="pymsk",
    version="0.1",
    author="Serena Bonaretti, more to come",
    author_email="serena.bonaretti.research@gmail.com",
    description="Package for musculoskeletal (MSK) image analysis",
    url="https://github.com/JCMSK/pyMSK",
    license="GNU General Public License v3 (GPLv3)",
    # including requirements (dependencies)
    install_requires=[
        l.strip() for l in
        Path('requirements.txt').read_text('utf-8').splitlines()
    ],
    # python version, license, and OS
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)

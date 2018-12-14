from pathlib import Path
from setuptools import setup


long_description = Path("README.md").read_text()

setup(
    name="fieldmaps",
    author="David Law",
    author_email="davidsamuellaw@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache Software License (Apache 2.0)",
    install_requires=["matplotlib>=2.0.2"],
    packages=["fieldmaps"],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Visualization",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)

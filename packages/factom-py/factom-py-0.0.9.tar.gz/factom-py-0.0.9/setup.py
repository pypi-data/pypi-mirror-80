from setuptools import (
    setup,
    find_packages,
)


deps = {"factom-py": ["factom-keys", "plyvel",], "hydra": ["bottle", "click", "plyvel", "requests",]}

setup(
    name="factom-py",
    version="0.0.9",
    description="A python library for working with the primitives of the Factom blockchain",
    author="Justin Hanneman (originally Sam Barnes)",
    author_email="justin@factom.com",
    url="https://github.com/FactomProject/factom-py",
    keywords=["factom", "core", "blockchain"],
    license="MIT",
    py_modules=["factom_py"],
    install_requires=deps["factom-py"],
    zip_safe=False,
    packages=find_packages(exclude=["tests", "tests.*", "hydra", "p2p"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)

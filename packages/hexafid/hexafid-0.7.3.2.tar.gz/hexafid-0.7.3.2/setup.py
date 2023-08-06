# MIT License
# Copyright (c) 2020 h3ky1

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hexafid",
    version="0.7.3.2",  # version standard https://semver.org/
    author="h3ky1",
    author_email="geohax0r@gmail.com",
    license="MIT",
    description="The Hexafid Cipher reference implementation",
    keywords="cipher cryptography education research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/hexafid/hexafid",
    python_requires=">=3.6",
    platforms=["OS Independent"],
    packages=setuptools.find_packages(exclude=("scratch",)),
    include_package_data=True,
    install_requires=[
        "click"
    ],
    entry_points="""
        [console_scripts]
        hexafid=hexafid.hexafid_cli:main
    """,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)

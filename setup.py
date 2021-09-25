import re

import setuptools

requirements = [
    "redis",
    "python-decouple==3.3",
    "python-dotenv==0.15.0",
    "cloudscraper",
    "aiofiles",
    "aiohttp",
]


with open("pyUltroid/version.py", "rt", encoding="utf8") as x:
    version = re.search(r'__version__ = "(.*?)"', x.read()).group(1)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

name = "py-Ultroid"
author = "TeamUltroid"
author_email = "teamultroid@protonmail.ch"
description = "A Secure and Powerful Python-Telethon Based Library For Ultroid Userbot."
license = "GNU AFFERO GENERAL PUBLIC LICENSE (v3)"
url = "https://github.com/TeamUltroid/pyUltroid"
project_urls = {
    "Bug Tracker": "https://github.com/TeamUltroid/pyUltroid/issues",
    "Documentation": "https://ultroid.tech",
    "Source Code": "https://github.com/TeamUltroid/pyUltroid",
}
classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
]

setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    project_urls=project_urls,
    license=license,
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=classifiers,
    python_requires=">=3.6",
)

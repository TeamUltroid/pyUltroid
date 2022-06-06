import os
import shutil

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

long_description = "# pyUltroid-fns"

name = "pyUltroid-fns"
author = "TeamUltroid"
author_email = "teamultroid@protonmail.ch"
description = "Function based library for telegram telethon projects."
license_ = "GNU AFFERO GENERAL PUBLIC LICENSE (v3)"

url = "https://github.com/TeamUltroid/pyUltroid"

project_urls = {
    "Bug Tracker": "https://github.com/TeamUltroid/pyUltroid/issues",
    "Documentation": "https://ultroid.tech",
    "Source Code": "https://github.com/TeamUltroid/pyUltroid",
}
classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
]

shutil.copy("pyUltroid/_misc/_wrappers.py", "pyUltroid/wrappers.py")
shutil.copy("pyUltroid/startup/_database.py", "pyUltroid/db.py")

setuptools.setup(
    name=name,
    version="0.0.1.b0",
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    project_urls=project_urls,
    license=license_,
    packages=setuptools.find_packages(
        exclude=["pyUltroid.dB", "pyUltroid._misc", "pyUltroid.startup"]
    ),
    install_requires=["telethon"],
    classifiers=classifiers,
    python_requires=">3.7, <3.11",
)

for file in ["wrappers", "db"]:
    os.remove(f"pyUltroid/{file}.py")

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

name = "pyUltroid"
version = "1.0.0"
author = "TeamUltroid"
author_email = "teamultroid@protonmail.ch"
description = "A Secure and Powerful Python-Telethon Based Library For Ultroid Userbot."
license = "GNU AFFERO GENERAL PUBLIC LICENSE (v3)"
url = "https://github.com/TeamUltroid/Ultroid"

setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    license=license,
    packages=setuptools.find_packages(),
    install_requires=[
        "telethon>=1.19.5",
        "redis",
        "python-decouple==3.3",
        "cryptg",
        "python-dotenv==0.15.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

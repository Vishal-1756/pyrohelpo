from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyrohelpo",
    version="4.1.5",
    author="Vishal-1756",
    author_email="vishalborse199@gmail.com",
    description="A powerful pagination library for Pyrogram bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vishal-1756/Helpo",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "kurigram",
        "tgcrypto",
    ],
    keywords=["pyrogram", "telegram", "bot", "pagination", "help-menu"],
)

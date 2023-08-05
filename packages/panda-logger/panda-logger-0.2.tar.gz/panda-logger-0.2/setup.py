from setuptools import setup
import re

with open("README.md", "r") as f:
    readme = f.read()

with open("panda_logger/__init__.py", "r") as f:
    regex = r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]'
    version = re.search(regex, f.read(), re.MULTILINE).group(1)

setup(
    name="panda-logger",
    version=version,
    packages=['panda_logger'],
    author="daiming",
    author_email="ming.dai@xiongmaols.com",
    description="A loguru instance init by toml file",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=["loguru>=0.5.1", "dynaconf>=3.1.0"],
    python_requires=">=3.5",
)
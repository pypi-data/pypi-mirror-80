from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="ghostport",
    version="0.0.4",
    packages=["ghostport"],
    description="GhostPort Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="GhostPort",
    author_email="admin@ghostport.io",
    license="MIT",
    url="https://github.com/ghostport/python-sdk",
    keywords=["feature", "flag", "ghostport"],
    install_requires=[
        'requests>=2.24.0',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

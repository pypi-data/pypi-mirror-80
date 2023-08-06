from setuptools import setup

with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(
    name="ansi-escape-sequences",
    version="0.0.2",
    description="Simple tool to use ansi escape sequences",
    py_mosules=["ansi_escape_sequences"],
    package_dir={'': "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ]
)

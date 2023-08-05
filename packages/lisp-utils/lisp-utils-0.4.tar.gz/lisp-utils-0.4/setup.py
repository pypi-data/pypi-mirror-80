import setuptools

with open("README-package.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lisp-utils", 
    version="0.4",
    author="Linkspirit Team",
    author_email="tecnici@linkspirit.it",
    description="This package contains some Linkspirit classes such as Database, Configuration.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.linkspirit.it/linkspirit/python-lisp-utils.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
	   'psycopg2-binary',
	],
    python_requires='>=3',
)

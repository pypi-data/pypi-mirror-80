from setuptools import setup, find_packages

with open("VERSION") as vfile:
    version_line = vfile.readline()

with open("README.md", "r") as fh:
    long_description = fh.read()

version = version_line.strip()

setup(
    name="metadocuments",
    py_modules=["metadocuments"],
    include_package_data=True,
    version=version,
    license="MIT",
    description="Library for defining structured documents (JSON, YAML) as classes. Created as a metaprogramming exercise",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Aki Mäkinen",
    author_email="nenshou.sora@gmail.com",
    url="https://gitlab.com/blissfulreboot/python/metadocuments",
    keywords=[],
    install_requires=[
        "pyaml"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ]
)


from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="japan-city-builder",
    version="0.1.0",
    author="masatori",
    description="A city-building simulation game set in Japan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/masatori/japan-city-builder",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pygame>=2.1.0",
        "numpy>=1.20.0",
        "Pillow>=9.0.0",
        "pyyaml>=6.0",
        "jsonschema>=4.0.0",
    ],
)

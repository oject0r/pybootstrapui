from setuptools import setup, find_packages

# Функция для чтения requirements.txt
def parse_requirements(filename):
    with open(filename, encoding="utf-8") as f:
        return f.read().splitlines()

setup(
    name="pybootstrapui",
    version="1.1.1",
    description="A Python library for building web interfaces with dynamic and desktop features.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="oject0r",
    author_email="hd076@protonmail.com",
    url="https://github.com/oject0r/pybootstrapui",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'typing_extensions',
        'aiohttp'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)

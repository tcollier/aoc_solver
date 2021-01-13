import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aoc-solver",
    version="0.0.13",
    author="Tom Collier",
    author_email="tcollier@gmail.com",
    description="Utility to run, test, and time Advent of Code solutions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tcollier/aoc_solver",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    entry_points={"console_scripts": ["aoc-solver=aoc_solver.exe:main"]},
)

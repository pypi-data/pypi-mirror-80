import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FrickDB",
    version="0.0.1",
    author="Harsh Vardhan",
    author_email="vardhan.harsh4041@gmail.com",
    description="A wierd JSON-based database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/4041RebL/FrickDB",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
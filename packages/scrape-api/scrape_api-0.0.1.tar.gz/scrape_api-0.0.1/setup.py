import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrape_api",
    version="0.0.1",
    author="Ali Haider",
    author_email="alinisarhaider@gmail.com",
    description="A Python wrapper for Reddit scraping API. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["scrape_api"],
    package_dir={'': 'src'},
    # url="https://github.com/alinisarhaider/ytkd_api",
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

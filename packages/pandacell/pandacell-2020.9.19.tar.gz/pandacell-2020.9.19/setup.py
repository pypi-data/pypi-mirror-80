from pathlib import Path

from setuptools import setup

here = Path(__file__).parent

with open(here / "README.md") as f:
    long_description = f.read()

setup(
    name="pandacell",
    use_calver=True,
    setup_requires=["calver"],
    description="IPython wrapper to more easily manipulate Pandas dataframes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eirki/pandacell",
    author="Eirik B. Stavestrand",
    author_email="eirik.b.stavest@gmail.com",
    license="MIT",
    py_modules=["pandacell"],
    keywords="pandas",
    classifiers=[
        # Intended Audience.
        "Intended Audience :: Developers",
        # Environment.
        "Environment :: Console",
        # License.
        "License :: OSI Approved :: MIT License",
        # Operating Systems.
        "Operating System :: OS Independent",
        # Supported Languages.
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=["ipython"],
)

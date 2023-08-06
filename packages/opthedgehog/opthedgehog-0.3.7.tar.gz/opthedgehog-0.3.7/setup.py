import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="opthedgehog",
    version="0.3.7",
    author="Linbo Shao",
    author_email="mail@linbo-shao.com",
    description="A python module to generate mask for integrated optics and acoustics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=["opthedgehog"],
    install_requires = [
        "numpy>=1.12.0",
        "bezier>=2020.5.19",
        "gdspy>=1.5.2,<1.6",
        "termcolor",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
)
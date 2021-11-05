import setuptools


with open("requirements.txt", "r") as fp:
    required = fp.read().splitlines()

setuptools.setup(
    name="omni",
    version="0.1.0",
    author="James Morrill",
    author_email="james.morrill.6@gmail.com",
    description="Omnipotent/omnipresent functions.",
    url="https://github.com/jambo6/omni",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=required,
    extras_require={
        "test": ["pytest"]
    }
)

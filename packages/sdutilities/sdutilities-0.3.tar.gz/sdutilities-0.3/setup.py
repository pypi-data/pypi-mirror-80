import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sdutilities",
    version="0.3",
    author="Stephen Olsen",
    author_email="stephenolsen@sociallydetermined.com",
    description="This package is intended to implement uniformity across SD Data Science projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orgs/SociallyDetermined/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

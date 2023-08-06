import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="git-adapter",
    version="0.2.4",
    author="Wolfgang Dobler",
    author_email="wdobler@gmail.com",
    description="A Python interface to the Git command line.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/wdobler/git-adapter.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.6.9',
)

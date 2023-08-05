import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-bufflog",
    version="0.0.2",
    author="David Gasquez",
    author_email="davidgasquez@buffer.com",
    description="Python logger for Buffer services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bufferapp/python-bufflog",
    install_requires=["structlog"],
    packages=setuptools.find_packages(),
)

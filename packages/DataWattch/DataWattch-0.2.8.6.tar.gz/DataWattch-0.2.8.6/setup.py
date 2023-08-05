import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DataWattch",  # Replace with your own username
    version="0.2.8.6",
    author="Daan Driessen",
    author_email="daan@ascos.nl",
    description="Driver for custom hardware for domoticz",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://test.pypi.org/project/DataWattch",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    install_requires=[
        "smbus2"
    ],
    python_requires='>=3.6',
)

import setuptools

with open("readme.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="flightaware-history-rolandcrosby",
    description="Retrieve flight track logs from FlightAware as KML files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rolandcrosby/flightaware-history",
    version="0.1.0",
    author="Roland Crosby",
    author_email="roland@rolandcrosby.com",
    license="0BSD",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=["lxml>=4.5", "MechanicalSoup>=0.12"],
    entry_points={
        "console_scripts": ["flightaware-history = flightaware_history.__main__:main"]
    },
)
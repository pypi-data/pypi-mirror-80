import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="routing_telethon",
    version="0.0.1",
    author="Arseny Tokmancev",
    description="A package with convenient routing for writing bots for Telethon",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Arseny-Tokmancev/telethon_routing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires =
        ['telethon >= 1.16.4',
        'sqlalchemy >= 1.3.19']
)

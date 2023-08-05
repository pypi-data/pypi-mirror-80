import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="PirxcyMethod",
    version="2.0",
    author="Pirxcy",
    description="PartyBot in a PyPi package form to easily be ran on repl.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xMistt/fortnitepy-bot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'crayons',
        'fortnitepy',
        'BenBotAsync',
        'FortniteAPIAsync',
        'uvloop',
        'sanic',
        'aiohttp'
    ],
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="expetator-gdacosta",
    version="0.0.1",
    author="Georges Da Costa",
    author_email="georges.da-costa@irit.fr",
    description="A framework for monitoring HPC applications using DVFS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/georges-da-costa/expetator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

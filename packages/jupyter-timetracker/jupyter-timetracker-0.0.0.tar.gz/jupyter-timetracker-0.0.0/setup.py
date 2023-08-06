
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jupyter-timetracker", 
    version="0.0.0",
    author="Prateek Kumar",
    author_email="prateekongithub@gmail.com",
    description="timelog is a powerful python library to track, manage and analyse your time",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PrateekKumarPython/timelog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LRstats",
    version="0.0.3",
    author="Salvatore Causio",
    author_email="salvatore.causio@cmcc.it",
    description="Computing statistic for longrun",
    long_description=long_description,
    packages=setuptools.find_packages(),
    url='https://gitlab.com/salvatore.causio/longrun_statistics.git',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
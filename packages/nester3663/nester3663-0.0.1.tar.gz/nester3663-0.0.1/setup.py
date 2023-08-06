from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name='nester3663',
        version='0.0.1',
        description='A very simple printer of nested lists',
        py_modules=["nester3663"],
        package_dir={'': 'src'},
        classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
        ],
        long_description=long_description,
        long_description_content_type="text/markdown",
        install_requires=[
            "blessings ~= 1.7",
        ],
        extras_require={
            "dev": [
                "pytest>=3.7",
            ],
        },
        url="https://github.com/honeywhisperer",
        author="Nikola Trailovic",
        author_email="nikola.trailovic@gmail.com",
    )
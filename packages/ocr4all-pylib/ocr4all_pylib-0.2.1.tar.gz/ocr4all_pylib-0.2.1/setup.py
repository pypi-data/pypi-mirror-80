from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ocr4all_pylib',
    version='0.2.1',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    author="Alexander Gehrke",
    author_email="alexander.gehrke@informatik.uni-wuerzburg.de",
    url="https://gitlab2.informatik.uni-wuerzburg.de/ocr4all-page-segmentation/pylib.git",
    install_requires=open("requirements.txt").read().split(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Image Recognition"
    ],
    keywords=['utility', 'page segmentation', 'image preprocessing'],
    data_files=[('', ["requirements.txt"])],
)

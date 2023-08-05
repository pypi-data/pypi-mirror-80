from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ocr4all_pixel_classifier_frontend',
    version='0.6.0',
    packages=find_packages(),
    long_description=long_description,

    long_description_content_type="text/markdown",
    include_package_data=True,
    author="Christoph Wick, Alexander Hartelt, Alexander Gehrke",
    author_email="christoph.wick@informatik.uni-wuerzburg.de, alexander.hartelt@informatik.uni-wuerzburg.de, alexander.gehrke@informatik.uni-wuerzburg.de",
    url="https://gitlab2.informatik.uni-wuerzburg.de/ocr4all-page-segmentation/ocr4all-pixel-classifier-frontend",
    entry_points={
        'console_scripts': [
            'ocr4all-pixel-classifier=ocr4all_pixel_classifier_frontend.main:main',
            'page-segmentation=ocr4all_pixel_classifier_frontend.main:main',  # legacy
        ],
    },
    install_requires=open("requirements.in").read().split(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Image Recognition"

    ],
    keywords=['OCR', 'page segmentation', 'pixel classifier'],
    data_files=[('', ["requirements.txt"])],
)

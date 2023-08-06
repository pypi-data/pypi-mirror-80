"""Setup.py for PyWatermark."""
from setuptools import setup, find_packages

with open("README.md", "r") as fileObj:
    longDescription = fileObj.read()

setup(
    name="PyWatermark",
    packages=find_packages(),
    version="0.1.4",
    author="Ieshaan Saxena",
    author_email="ieshaan1999@gmail.com",
    description="A library to watermark your images easily.",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/ieshaan12/watermark",
    download_url="https://github.com/ieshaan12/watermark/archive/v0.1.4.tar.gz",
    package_data={
        'PyWatermark': [
            'fonts/Bangers-Regular.ttf', 'fonts/MerriweatherSans-Regular.ttf',
            'fonts/Oswald-Regular.ttf', 'fonts/Raleway-Regular.ttf',
            'fonts/Roboto-Regular.ttf'
        ]
    },
    install_requires=['pillow>=7.2.0'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

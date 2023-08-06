from setuptools import setup
from setuptools import find_packages


NAME = "ashe"
VERSION = "0.0.3"
AUTHOR = "Ailln"
EMAIL = "kinggreenhall@gmail.com"
URL = "https://github.com/Ailln/ashe"
LICENSE = "MIT License"
DESCRIPTION = "ashe is super extension of Python."

if __name__ == "__main__":
    setup(
        name=NAME,
        version=VERSION,
        author=AUTHOR,
        author_email=EMAIL,
        url=URL,
        license=LICENSE,
        description=DESCRIPTION,
        packages=find_packages(),
        include_package_data=True,
        install_requires=open("./requirements.txt", "r").read().splitlines(),
        long_description=open("./README.md", "r").read(),
        long_description_content_type='text/markdown',
        zip_safe=True,
        classifiers=[
            "Programming Language :: Python :: 3",
            f"License :: OSI Approved :: {LICENSE}",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.6"
    )

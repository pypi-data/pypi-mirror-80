import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="micro-lisp-tool-amotzek",
    version="1.0." + os.environ["BITBUCKET_BUILD_NUMBER"],
    author="Andreas Motzek",
    author_email="andreas-motzek@t-online.de",
    description="Run and upload Lisp programs and use the read-eval-print loop with ESP32 boards flashed with Micro Lisp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/amotzek/micro-lisp-tool/src/master/",
    packages=setuptools.find_packages(),
    install_requires=["pyserial>=3.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Terminals :: Serial"
    ],
    python_requires=">=3.6"
)

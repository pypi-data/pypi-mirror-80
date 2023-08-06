# System Imports
import ast
import io
import re
import os
from setuptools import find_packages, setup

# Framework / Library Imports

# Application Imports

# Local Imports

DEPENDENCIES = [
    "influxdb==5.2.3",
    "speedtest-cli==2.1.2",
    "schedule==0.6.0"
]
EXCLUDE_FROM_PACKAGES = ["contrib", "docs", "tests*"]
CURDIR = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()

def get_version():
    main_file = os.path.join(CURDIR, "speedtest_influx_logger", "main.py")
    _version_re = re.compile(r"APP_VERSION\s+=\s+(?P<version>.*)")
    with open(main_file, "r", encoding="utf8") as f:
        match = _version_re.search(f.read())
        version = match.group("version") if match is not None else '"unknown"'
    return str(ast.literal_eval(version))

setup(
    name="speedtest_influx_logger",
    version=get_version(),
    author="Dan Streeter",
    author_email="dan@danstreeter.co.uk",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/danstreeter/speedtest-logger",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    keywords=[],
    scripts=[],
    entry_points={"console_scripts": ["speedtest_influx=speedtest_influx_logger.main:main"]},
    zip_safe=False,
    install_requires=DEPENDENCIES,
    test_suite="tests.test_project",
    python_requires=">=3.7",
    # license and classifier list:
    # https://pypi.org/pypi?%3Aaction=list_classifiers
    license="License :: OSI Approved :: MIT License",
    classifiers=[
        "Programming Language :: Python",
        # "Programming Language :: Python :: 3",
        # "Operating System :: OS Independent",
        # "Private :: Do Not Upload"
    ],
)
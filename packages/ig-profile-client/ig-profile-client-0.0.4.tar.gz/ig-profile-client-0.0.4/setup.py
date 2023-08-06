from setuptools import setup, find_packages
import re

with open('IgProfileClient/version.py', 'r') as version_file:
    version_match = re.search(r"^VERSION ?= ?['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    version = version_match.group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'requests'
]

test_requirements = [
    'coverage', 'wheel', 'pytest', 'requests_mock'
]

classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Development Status :: 3 - Alpha"
]

setup(
    name="ig-profile-client",
    version=version,
    author="Panchorn Lertvipada",
    author_email="nonpcn@gmail.com",
    description="A common client to get instagram profile (public data)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Panchorn/ig-profile-client.git",
    license="MIT",
    packages=find_packages(),
    package_dir={'ig-profile-client': 'IgProfileClient'},
    install_requires=requirements,
    tests_require=test_requirements,
    classifiers=classifiers
)

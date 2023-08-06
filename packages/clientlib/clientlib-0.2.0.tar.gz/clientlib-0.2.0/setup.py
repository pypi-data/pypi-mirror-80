from setuptools import setup, find_packages


def get_requirements():
    with open("requirements.txt") as f:
        requirements = [
            line.strip()
            for line in f
        ]

    return requirements


def get_test_requirements():
    with open("requirements-test.txt") as f:
        requirements = [
            line.strip()
            for line in f
        ]

    return requirements


def get_long_description():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name='clientlib',
    version='0.2.0',
    author="Panagiotis Matigakis",
    author_email="pmatigakis@gmail.com",
    description="HTTP API client framework",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/pmatigakis/clientlib",
    packages=find_packages(exclude=["tests"]),
    install_requires=get_requirements(),
    tests_require=get_test_requirements(),
    test_suite='nose.collector',
    include_package_data=True,
    zip_safe=True,
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries"
    )
)

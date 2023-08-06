from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.read()

setup_requirements = ["pytest-runner", "flake8"]

test_requirements = ["coverage", "pytest", "pytest-cov", "pytest-mock"]

setup(
    author="Eduardo Gonzalez Solares",
    author_email="eglez@ast.cam.ac.uk",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
    ],
    description="IMAXT Machine Learning Tools",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme,
    include_package_data=True,
    keywords="imaxt, ml",
    name="imaxtml",
    packages=find_packages(include=["imaxtml*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/IMAXT/imaxtml",
    download_url="https://github.com/IMAXT/imaxtml/archive/v0.0.2.tar.gz",
    version="0.0.2",
    zip_safe=False,
    python_requires=">=3",
)

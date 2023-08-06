from setuptools import setup, find_packages

setup(
    name="reportxl",
    version="0.1",
    author="Brendon Lin",
    author_email="brendon.lin@outlook.com",
    description="Use Excel to make a report.",
    # packages=["reportxl"],
    packages=find_packages(exclude=["tests"]),
    install_requires=["openpyxl>=3.0.5"],
    entry_points={"console_scripts": ["runit = package.view:main"]},
)

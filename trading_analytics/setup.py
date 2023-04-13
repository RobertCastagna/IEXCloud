from setuptools import find_packages, setup

setup(
    name="trading_analytics",
    packages=find_packages(exclude=["trading_analytics_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)

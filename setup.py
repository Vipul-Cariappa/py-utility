from setuptools import setup, find_packages


setup(
    name="py-utility",
    version="0.1.1",
    description="Utility functions for managing and monitoring python resources",
    long_description="Utility functions for managing and monitoring python resources",
    url="https://github.com/Vipul-Cariappa/py-utility",
    author="Vipul Cariappa",
    author_email="vipulcariappa@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="py-utility",
    packages=find_packages(exclude=["tests/"]),
    install_requires=[],
    test_suite='tests',
    tests_require="pytest",
    python_requires='>=3.6',
)

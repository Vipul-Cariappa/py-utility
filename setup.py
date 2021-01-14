from setuptools import setup, find_packages


setup(
    name="py-utility",
    version="0.1.3",
    description="Utility functions for managing and monitoring python resources",
    long_description="Utility functions for managing and monitoring python resources",
    url="https://github.com/Vipul-Cariappa/py-utility",
    author="Vipul Cariappa",
    author_email="vipulcariappa@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        # "Intended Audience:: Developers",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        # "Topic :: Utilities",
    ],
    keywords="py-utility",
    packages=find_packages(exclude=["tests/"]),
    install_requires=[
        "pywin32;sys_platform=='win32'"
    ],
    test_suite='tests',
    tests_require="pytest",
    python_requires='>=3.6',
)

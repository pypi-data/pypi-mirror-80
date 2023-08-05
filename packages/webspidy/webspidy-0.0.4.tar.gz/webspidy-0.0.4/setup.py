from setuptools import setup, find_packages


setup(
    name="webspidy",
    version="0.0.4",
    description="A human friendly web crawling library",
    py_module=["webspidy"],
    license="MIT",
    keywords="web,spider,crawler",
    packages=find_packages(),
    install_requires=[
        "bs4>=0.0.1",
        "requests>=2.24.0"
    ],
    extras_require={
        "dev": [
            "pytest>=3.7",
            "check-manifest>=0.43",
            "twine>=3.2.0"
        ]
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],

    url="https://github.com/anyms/webspidy",
    author="Jeeva",
    author_email="tellspidy@gmail.com"
)

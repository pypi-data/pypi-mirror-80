import setuptools

requires = [
    'print-table>=1.2.1'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="storekeys",
    version="1.7.1",
    author="noidea",
    author_email="noidea1238@gmail.com",
    description="Simple package to store values at a single place",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requires,
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['storekeys=storekeys.store:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

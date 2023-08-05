import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stockie", 
    version="0.0.6",
    author="Suparjo Tamin",
    author_email="suparjo.tamin@gmail.com",
    description="A package to identify stock candlestick pattern",
    long_description=long_description,
    url="https://github.com/suparjotamin/stocky",
    packages=setuptools.find_packages(),
    package_data = {
        '': ['pattern_img.json','pattern_type.json']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['yfinance', 'mpl_finance'],
)

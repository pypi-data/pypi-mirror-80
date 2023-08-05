import setuptools

def readme():
	with open("README.md") as f:
		README = f.read()
	return README

setuptools.setup(
    name="loanpy",
    version="0.0.7",
    author="Viktor Martinović",
    author_email="viktor.martinovic@hotmail.com",
    description="framework for detecting old loanwords",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/martino-vic/Framework-for-computer-aided-borrowing-detection",
    license="Creative Commons Attribution 4.0 International",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Academic Free License (AFL)",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    packages=["loan_py"],
    include_package_data=True,
    install_requires=["pandas","lingpy","nltk","epitran","gensim","bs4","pdfminer"],
    python_requires='>=3.6',
)
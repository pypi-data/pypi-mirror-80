from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="IntrinsicAnalysis",
    version="0.0.1",
    author="Ariana Asatryan, Tsolak Ghukasyan, Yeva Yeshilbashian",
    description="Intrinsic analysis package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arianasatryan/IntrinsicAnalysis.git",
    install_requires=['googledrivedownloader==0.4', 'stanza>=1.0.1"', 'spacy-udpipe>=0.3.1', 'nltk', 'scikit-learn'],
    include_package_data=True,
    packages=["IntrinsicAnalysis", "IntrinsicAnalysis.feature_extractors", "IntrinsicAnalysis.clustering"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ]
)

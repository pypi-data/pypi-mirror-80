from distutils.core import setup

setup(
    name="nspywrapper",
    packages=["nspywrapper"],
    version="0.3.2",
    license="Apache",
    description="A python wrapper for the NationStates API",
    long_description="See here for more information: https://github.com/abrow425/nspy_wrapper",
    author="Andrew Brown (aka SherpDaWerp)",
    author_email="abrow425@gmail.com",
    url="https://github.com/abrow425/nspy_wrapper",
    download_url="https://github.com/abrow425/nspy_wrapper/archive/v0.3.2.tar.gz",
    keywords=["NATIONSTATES", "NS", "API", "WRAPPER"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        "urllib3",
    ],
)

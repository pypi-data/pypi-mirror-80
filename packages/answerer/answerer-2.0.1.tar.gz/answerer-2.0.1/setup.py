from distutils.core import setup

setup(
    name="answerer",
    packages=["answerer"],
    version="2.0.1",
    license="Apache",
    description="A system that outputs a nice list of links to speed up issues answering.",
    long_description="See here for more information: https://github.com/abrow425/gotIssues",
    author="Andrew Brown (aka SherpDaWerp)",
    author_email="abrow425@gmail.com",
    url="https://github.com/abrow425/gotIssues",
    download_url="https://github.com/abrow425/gotIssues/archive/v2.0.1.tar.gz",
    keywords=["NATIONSTATES", "NS", "API"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        "nspy_wrapper",
        "urllib3",
    ],
)

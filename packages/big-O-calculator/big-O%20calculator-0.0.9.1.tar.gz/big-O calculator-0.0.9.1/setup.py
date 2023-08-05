from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="big-O calculator",
    version="0.0.9.1",
    description="A calculator to predict big-O of sorting functions",
    url="https://github.com/Alfex4936",
    author="Seok Won",
    author_email="ikr@kakao.com",
    license="MIT",
    packages=["bigO"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.5",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["win10toast"],
    zip_safe=False,
    setup_requires=["pytest-runner", "flake8"],
    tests_require=["pytest"],
)

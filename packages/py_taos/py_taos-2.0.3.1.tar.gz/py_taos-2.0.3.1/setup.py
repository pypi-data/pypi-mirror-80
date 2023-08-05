import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_taos",
    version="2.0.3.1",
    author="Taosdata Inc.",
    author_email="support@taosdata.com",
    description="TDengine python client package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/evoup/py-taos",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
)

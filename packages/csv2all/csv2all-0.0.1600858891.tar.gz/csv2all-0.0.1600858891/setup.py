import setuptools
import time

v_time = str(int(time.time()))

with open("../README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as r:
    requirements = r.read().split("\n")[0:-1]

setuptools.setup(
    name="csv2all",
    version="0.0."+v_time,
    author="Daniel Doña Álvarez",
    author_email="daniel.dona@xnor.ga",
    license="Apache 2.0",
    description="Memory constrained CSV to JSON and XML converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daniel-dona/csv2all",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.6',
)

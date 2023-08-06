from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='jesuslama',
    version='0.0.1',
    description='Say, hello!',
    py_modules=["helloworld"],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dylanballback/packagetest",
    author="Dylan Ballback",
    author_email="Dylanballback19@gmail.com",
)

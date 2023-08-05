import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='estore-base',
    version='0.0.6',
    description='Event Store Base Classes',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lostwire/estore-common", 
    author='Jnxy',
    author_email='jnxy@lostwire.net',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: AsyncIO",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Database" ],
    packages=setuptools.find_namespace_packages(include=['estore.*']))
